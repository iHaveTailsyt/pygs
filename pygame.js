const fs = require('fs');
const esprima = require('esprima');

class PyGameInterpreter {
  constructor() {
    this.scope = {};
  }

  visit(node) {
    if (node.type === 'Program') {
      node.body.forEach(statement => this.visit(statement));
    } else if (node.type === 'VariableDeclaration') {
      node.declarations.forEach(declaration => {
        this.scope[declaration.id.name] = this.visit(declaration.init);
      });
    } else if (node.type === 'Literal') {
      return node.value;
    } else if (node.type === 'Identifier') {
      return this.scope[node.name];
    } else if (node.type === 'BinaryExpression') {
      const left = this.visit(node.left);
      const right = this.visit(node.right);

      switch (node.operator) {
        case '+':
          return left + right;
        case '-':
          return left - right;
        case '*':
          return left * right;
        case '/':
          return left / right;
        default:
          throw new Error(`Unsupported operator: ${node.operator}`);
      }
    } else if (node.type === 'ExpressionStatement') {
      this.visit(node.expression);
    } else if (node.type === 'AssignmentExpression') {
      const variableName = node.left.name;
      const value = this.visit(node.right);
      this.scope[variableName] = value;
    } else if (node.type === 'CallExpression' && node.callee.name === 'print') {
      node.arguments.forEach(arg => {
        const value = this.visit(arg);
        process.stdout.write(value + ' ');
      });
      process.stdout.write('\n');
    } else {
      throw new Error(`Unsupported node type: ${node.type}`);
    }
  }

  runPyGameScript(code) {
    const ast = esprima.parseScript(code);
    this.visit(ast);
  }
}

function runPyGameScriptFromFile(filename) {
  const code = fs.readFileSync(filename, 'utf-8');
  const interpreter = new PyGameInterpreter();
  interpreter.runPyGameScript(code);
}

if (process.argv.length !== 3) {
  console.error('Usage: node pygameinterpreter.js your_script.pygs');
  process.exit(1);
}

runPyGameScriptFromFile(process.argv[2]);
