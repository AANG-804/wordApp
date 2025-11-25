import SwiftUI

struct ContentView: View {
    @StateObject private var networkManager = NetworkManager()
    @State private var searchText = ""
    @State private var isPinned = false
    
    var body: some View {
        VStack(spacing: 20) {
            // Header
            VStack {
                HStack {
                    Text("WordApp Dictionary")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                    
                    Spacer()
                    
                    Button(action: {
                        isPinned.toggle()
                    }) {
                        Image(systemName: isPinned ? "pin.fill" : "pin")
                            .foregroundColor(isPinned ? .accentColor : .secondary)
                            .font(.title2)
                    }
                    .buttonStyle(.plain)
                    .help(isPinned ? "Unpin from top" : "Pin to top")
                    .onChange(of: isPinned) { newValue in
                        if let window = NSApp.windows.first(where: { $0.isKeyWindow }) {
                            window.level = newValue ? .floating : .normal
                        }
                    }
                }
                .padding(.horizontal)
            }
            .padding(.top)
            
            // Search Bar
            HStack {
                TextField("Enter a word...", text: $searchText)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .onSubmit {
                        if !searchText.isEmpty {
                            networkManager.lookupWord(word: searchText)
                            searchText = "" // Clear text after search
                        }
                    }
                
                Button(action: {
                    if !searchText.isEmpty {
                        networkManager.lookupWord(word: searchText)
                        searchText = "" // Clear text after search
                    }
                }) {
                    Text("Search")
                }
                .disabled(searchText.isEmpty)
                
                Button(action: {
                    networkManager.resetHistory()
                }) {
                    Image(systemName: "trash")
                        .foregroundColor(.red)
                }
                .disabled(networkManager.history.isEmpty)
                .help("Reset History")
            }
            .padding(.horizontal)
            
            // Global Error Message (Rate Limit etc.)
            if let globalError = networkManager.globalErrorMessage {
                Text(globalError)
                    .foregroundColor(.red)
                    .font(.caption)
                    .padding(.horizontal)
                    .transition(.opacity)
            }
            
            // Content
            ScrollView {
                VStack(spacing: 20) {
                    ForEach(networkManager.history.reversed(), id: \.id) { item in
                        VStack {
                            switch item.status {
                            case .loading:
                                VStack(spacing: 12) {
                                    ProgressView()
                                    Text("Looking up '\(item.query)'...")
                                        .foregroundColor(.secondary)
                                }
                                .frame(maxWidth: .infinity)
                                .padding()
                                .background(Color(nsColor: .controlBackgroundColor))
                                .cornerRadius(12)
                                .shadow(radius: 2)
                                
                            case .error(let errorMessage):
                                VStack(spacing: 8) {
                                    Text("🚫 WordApp은 영어 단어 검색기 입니다! 영어 단어를 입력주세요")
                                        .font(.headline)
                                        .foregroundColor(.red)
                                        .multilineTextAlignment(.center)
                                    
                                    Text(errorMessage)
                                        .font(.subheadline)
                                        .foregroundColor(.red.opacity(0.8))
                                    
                                    Text("Query: \(item.query)")
                                        .font(.caption)
                                        .foregroundColor(.secondary)
                                }
                                .padding()
                                .frame(maxWidth: .infinity)
                                .background(Color.red.opacity(0.1))
                                .cornerRadius(12)
                                .overlay(
                                    RoundedRectangle(cornerRadius: 12)
                                        .stroke(Color.red.opacity(0.3), lineWidth: 1)
                                )
                                
                            case .success(let definition):
                                VStack(alignment: .leading, spacing: 16) {
                                    // Word & Pronunciation
                                    HStack(alignment: .firstTextBaseline) {
                                        Text(definition.word)
                                            .font(.system(size: 32, weight: .bold))
                                        
                                        Text("[\(definition.pronunciation_ipa)]")
                                            .font(.title3)
                                            .foregroundColor(.secondary)
                                        
                                        Text("(\(definition.pronunciation_kr))")
                                            .font(.title3)
                                            .foregroundColor(.secondary)
                                    }
                                    
                                    Divider()
                                    
                                    // Meaning
                                    VStack(alignment: .leading, spacing: 8) {
                                        Text("Meaning")
                                            .font(.headline)
                                        Text(definition.meaning)
                                            .font(.body)
                                    }
                                    
                                    // Examples
                                    VStack(alignment: .leading, spacing: 12) {
                                        Text("Examples")
                                            .font(.headline)
                                        
                                        ForEach(definition.examples, id: \.self) { example in
                                            Text("• " + example)
                                                .font(.body)
                                                .padding(.bottom, 2)
                                        }
                                    }
                                    
                                    Divider()
                                    
                                    // Save Button & Status
                                    VStack(spacing: 8) {
                                        HStack {
                                            Spacer()
                                            Button(action: {
                                                networkManager.saveToNotion(item: item)
                                            }) {
                                                Label("Save to Notion", systemImage: "square.and.arrow.down")
                                                    .padding(.horizontal)
                                                    .padding(.vertical, 8)
                                            }
                                            .buttonStyle(.borderedProminent)
                                            Spacer()
                                        }
                                        
                                        if let saveStatus = item.saveStatus {
                                            Text(saveStatus)
                                                .font(.caption)
                                                .foregroundColor(saveStatus.contains("Success") ? .green : .red)
                                                .transition(.opacity)
                                        }
                                    }
                                }
                                .padding()
                                .background(Color(nsColor: .controlBackgroundColor))
                                .cornerRadius(12)
                                .shadow(radius: 2)
                            }
                        }
                        .padding(.horizontal)
                        .overlay(
                            Button(action: {
                                networkManager.removeDefinition(id: item.id)
                            }) {
                                Image(systemName: "xmark")
                                    .font(.system(size: 10, weight: .bold))
                                    .foregroundColor(.secondary)
                                    .padding(6)
                                    .background(Color.gray.opacity(0.1))
                                    .clipShape(Circle())
                            }
                            .buttonStyle(.plain)
                            .padding([.top, .trailing], 12),
                            alignment: .topTrailing
                        )
                    }
                    
                    if networkManager.history.isEmpty {
                        VStack {
                            Spacer()
                            Text("Enter a word to get started")
                                .foregroundColor(.secondary)
                                .padding(.top, 50)
                            Spacer()
                        }
                    }
                }
                .padding(.bottom)
            }
            
            // Copyright
            Text("© 2025 Jay. All rights reserved.")
                .font(.caption2)
                .foregroundColor(.secondary)
                .padding(.bottom, 8)
        }
        .frame(minWidth: 600, minHeight: 400)
        .padding()
    }
}

#Preview {
    ContentView()
}
