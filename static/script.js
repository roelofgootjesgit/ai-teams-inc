const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

function addMessage(content, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const label = document.createElement('div');
    label.className = 'message-label';
    label.textContent = sender === 'user' ? 'You' : 'AI Team';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // Check if content contains multi-agent responses
    if (sender === 'assistant' && content.includes('===')) {
        // Multi-agent response - parse and format
        contentDiv.innerHTML = parseMultiAgentResponse(content);
    } else {
        // Simple response
        contentDiv.textContent = content;
    }
    
    messageDiv.appendChild(label);
    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function parseMultiAgentResponse(content) {
    console.log('🔍 Parsing multi-agent response...');
    console.log('Content length:', content.length);
    console.log('Contains ===:', content.includes('==='));
    console.log('First 200 chars:', content.substring(0, 200));
    
    // Check if this looks like a multi-agent response
    if (!content.includes('🎯') && !content.includes('🏗️') && !content.includes('💼')) {
        console.log('❌ No agent icons found, showing as plain text');
        return content;
    }
    
    // Split by exactly 60 equals signs
    const sections = content.split(/={60}/);
    console.log('📊 Found sections:', sections.length);
    
    let html = '<div class="multi-agent-response">';
    let agentCount = 0;
    
    sections.forEach((section, index) => {
        const trimmed = section.trim();
        if (!trimmed) {
            console.log(`Section ${index}: Empty, skipping`);
            return;
        }
        
        console.log(`Section ${index}:`, trimmed.substring(0, 100));
        
        // Split into lines
        const lines = trimmed.split('\n');
        
        // First line should be: icon + agent name
        const headerLine = lines[0].trim();
        console.log('Header line:', headerLine);
        
        // Extract icon and agent name (more flexible regex - no ^ anchor)
        const match = headerLine.match(/([🎯🏗️💼])\s+(.+)/);
        
        if (match) {
            agentCount++;
            const icon = match[1];
            const agentName = match[2];
            
            console.log(`✅ Agent ${agentCount}: ${agentName}`);
            
            // Find where content starts (after the dashed line)
            let contentStartIndex = 1;
            for (let i = 1; i < lines.length; i++) {
                if (lines[i].includes('---')) {
                    contentStartIndex = i + 1;
                    break;
                }
            }
            
            // Get content (everything after dashed line)
            const agentContent = lines.slice(contentStartIndex).join('\n').trim();
            
            // Determine agent class for styling
            let agentClass = 'agent-response';
            if (agentName.includes('PROJECT MANAGER')) {
                agentClass += ' pm-response';
            } else if (agentName.includes('AI ARCHITECT')) {
                agentClass += ' architect-response';
            } else if (agentName.includes('DOMAIN EXPERT')) {
                agentClass += ' expert-response';
            }
            
            html += `
                <div class="${agentClass}">
                    <div class="agent-header">
                        <span class="agent-icon">${icon}</span>
                        <span class="agent-name">${agentName}</span>
                    </div>
                    <div class="agent-content">${agentContent}</div>
                </div>
            `;
        } else {
            console.log('❌ No match for header:', headerLine);
        }
    });
    
    html += '</div>';
    
    console.log(`✅ Parsed ${agentCount} agents`);
    
    return html;
}

function addLoadingIndicator() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    messageDiv.id = 'loading-message';
    
    const label = document.createElement('div');
    label.className = 'message-label';
    label.textContent = 'AI Team';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = '<span class="loading"></span> Team is discussing... (this may take 30-45 seconds)';
    
    messageDiv.appendChild(label);
    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);
    
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function removeLoadingIndicator() {
    const loading = document.getElementById('loading-message');
    if (loading) loading.remove();
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    
    // Disable input
    sendBtn.disabled = true;
    userInput.disabled = true;
    
    // Show user message
    addMessage(message, 'user');
    userInput.value = '';
    
    // Show loading
    addLoadingIndicator();
    
    try {
        // Increase timeout for multi-agent responses (60 seconds)
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 60000);
        
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message }),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Remove loading and show response
        removeLoadingIndicator();
        addMessage(data.response, 'assistant');
        
    } catch (error) {
        removeLoadingIndicator();
        if (error.name === 'AbortError') {
            addMessage('Response took too long. The AI team might be processing a complex request. Please try again.', 'assistant');
        } else {
            addMessage('Error: Could not connect to AI team. ' + error.message, 'assistant');
        }
        console.error(error);
    } finally {
        // Re-enable input
        sendBtn.disabled = false;
        userInput.disabled = false;
        userInput.focus();
    }
}

// Send on Enter (Shift+Enter for newline)
userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Initial greeting
window.onload = () => {
    addMessage('Hello! I am your AI Team with DISCUSSION capabilities:\n\n🎯 Project Manager - Coordinates & synthesizes\n🏗️ AI Architect - Technical expertise\n💼 Domain Expert - Business perspective\n\nAgents will DISCUSS your question, building on each other\'s insights. This takes 30-45 seconds but provides deeper analysis!\n\nAsk me anything!', 'assistant');
};