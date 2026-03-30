// Cream Language — VS Code Extension
// MauyaApps | creamlang.org

const vscode = require('vscode');

function activate(context) {
    console.log('Cream Language extension activated');

    // Status bar item
    const statusBar = vscode.window.createStatusBarItem(
        vscode.StatusBarAlignment.Left, 100
    );
    statusBar.text = '$(code) Cream';
    statusBar.tooltip = 'Cream Language — creamlang.org';

    // Show status bar when .cream file is open
    context.subscriptions.push(
        vscode.window.onDidChangeActiveTextEditor(editor => {
            if (editor && editor.document.languageId === 'cream') {
                statusBar.show();
            } else {
                statusBar.hide();
            }
        })
    );

    // Run Cream file command
    const runCmd = vscode.commands.registerCommand('cream.runFile', () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) return;

        const file = editor.document.fileName;
        const terminal = vscode.window.createTerminal('Cream');
        terminal.show();
        terminal.sendText(`cream "${file}"`);
    });

    // New Cream file command
    const newCmd = vscode.commands.registerCommand('cream.newFile', async () => {
        const doc = await vscode.workspace.openTextDocument({
            language: 'cream',
            content: '-- New Cream file\nname = "World"\nsay "Hello, {name}!"\n'
        });
        vscode.window.showTextDocument(doc);
    });

    context.subscriptions.push(statusBar, runCmd, newCmd);
}

function deactivate() {}

module.exports = { activate, deactivate };
