import Foundation
import Combine

struct WordDefinition: Codable, Equatable {
    let word: String
    let pronunciation_ipa: String
    let pronunciation_kr: String
    let meaning: String
    let examples: [String]
}

struct SaveRequest: Codable {
    let definition: WordDefinition
}

struct ErrorResponse: Codable {
    let detail: String
}

enum SearchStatus: Equatable {
    case loading
    case success(WordDefinition)
    case error(String)
}

struct SearchItem: Identifiable, Equatable {
    let id = UUID()
    let query: String
    var status: SearchStatus
    var saveStatus: String? = nil
    
    static func == (lhs: SearchItem, rhs: SearchItem) -> Bool {
        return lhs.id == rhs.id && lhs.status == rhs.status && lhs.saveStatus == rhs.saveStatus
    }
}

class NetworkManager: ObservableObject {
    @Published var history: [SearchItem] = []
    @Published var globalErrorMessage: String? // For rate limit errors etc.
    
    private let baseURL = "http://localhost:8000"
    private var requestTimestamps: [Date] = []
    private let maxRequests = 5
    private let timeWindow: TimeInterval = 10.0
    
    func lookupWord(word: String) {
        // Rate Limiting Check
        let now = Date()
        requestTimestamps = requestTimestamps.filter { now.timeIntervalSince($0) < timeWindow }
        
        if requestTimestamps.count >= maxRequests {
            globalErrorMessage = "Rate limit exceeded: Please wait a moment before searching again."
            // Clear error after 3 seconds
            DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
                if self.globalErrorMessage?.starts(with: "Rate limit") == true {
                    self.globalErrorMessage = nil
                }
            }
            return
        }
        
        requestTimestamps.append(now)
        globalErrorMessage = nil
        
        // Add Loading Card
        let newItem = SearchItem(query: word, status: .loading)
        history.append(newItem)
        
        guard let url = URL(string: "\(baseURL)/lookup") else {
            updateItemStatus(id: newItem.id, status: .error("Invalid URL"))
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body = ["word": word]
        request.httpBody = try? JSONSerialization.data(withJSONObject: body)
        
        URLSession.shared.dataTask(with: request) { [weak self] data, response, error in
            DispatchQueue.main.async {
                guard let self = self else { return }
                
                if let error = error {
                    self.updateItemStatus(id: newItem.id, status: .error("Error: \(error.localizedDescription)"))
                    return
                }
                
                guard let httpResponse = response as? HTTPURLResponse else {
                    self.updateItemStatus(id: newItem.id, status: .error("Invalid response"))
                    return
                }
                
                if httpResponse.statusCode == 400 {
                    if let data = data, let errorResponse = try? JSONDecoder().decode(ErrorResponse.self, from: data) {
                        self.updateItemStatus(id: newItem.id, status: .error(errorResponse.detail))
                    } else {
                        self.updateItemStatus(id: newItem.id, status: .error("Invalid input"))
                    }
                    return
                }
                
                guard let data = data else {
                    self.updateItemStatus(id: newItem.id, status: .error("No data received"))
                    return
                }
                
                do {
                    let decodedResponse = try JSONDecoder().decode(WordDefinition.self, from: data)
                    self.updateItemStatus(id: newItem.id, status: .success(decodedResponse))
                } catch {
                    self.updateItemStatus(id: newItem.id, status: .error("Decoding error: \(error.localizedDescription)"))
                }
            }
        }.resume()
    }
    
    private func updateItemStatus(id: UUID, status: SearchStatus) {
        if let index = history.firstIndex(where: { $0.id == id }) {
            history[index].status = status
        }
    }
    
    func resetHistory() {
        history.removeAll()
        globalErrorMessage = nil
    }
    
    func removeDefinition(id: UUID) {
        if let index = history.firstIndex(where: { $0.id == id }) {
            history.remove(at: index)
        }
    }
    
    func saveToNotion(item: SearchItem) {
        guard case let .success(definition) = item.status else { return }
        guard let url = URL(string: "\(baseURL)/save") else { return }
        
        // Update status to "Saving..."
        updateSaveStatus(id: item.id, message: "Saving...")
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let saveReq = SaveRequest(definition: definition)
        request.httpBody = try? JSONEncoder().encode(saveReq)
        
        URLSession.shared.dataTask(with: request) { [weak self] data, response, error in
            DispatchQueue.main.async {
                guard let self = self else { return }
                
                let message: String
                if let error = error {
                    message = "Save failed: \(error.localizedDescription)"
                } else if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 {
                    message = "Successfully saved to Notion!"
                } else {
                    message = "Failed to save to Notion"
                }
                
                self.updateSaveStatus(id: item.id, message: message)
                
                // Clear message after 3 seconds
                DispatchQueue.main.asyncAfter(deadline: .now() + 3) {
                    self.updateSaveStatus(id: item.id, message: nil)
                }
            }
        }.resume()
    }
    
    private func updateSaveStatus(id: UUID, message: String?) {
        if let index = history.firstIndex(where: { $0.id == id }) {
            history[index].saveStatus = message
        }
    }
}
