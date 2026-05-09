const { spawn } = require('child_process');

const child = spawn('bunx', ['apple-mcp@latest'], {
  stdio: ['pipe', 'pipe', 'inherit'],
});

child.stdout.on('data', (data) => {
  console.log('[RESPONSE]', data.toString());
});

// Construct the MCP tool call
const mcpCall = {
  tool: 'notes.search',
  args: {
    query: 'test',
  },
};

// Wait a bit for startup, then send the call
setTimeout(() => {
  console.log('[SEND]', JSON.stringify(mcpCall));
  child.stdin.write(JSON.stringify(mcpCall) + '\n');
}, 2000);

// Optional: exit after 5 seconds
setTimeout(() => {
  console.log('[EXITING]');
  child.kill();
}, 5000);