# AST Modification Skill

## Description
Semantic code parsing and modification using Tree-sitter for safe, syntax-aware transformations of JavaScript configuration files.

## Capabilities
- Parse JavaScript/TypeScript source code to Abstract Syntax Tree (AST)
- Query AST using S-expression syntax
- Locate specific function calls and object literals
- Insert and modify properties in objects
- Handle various code formatting styles
- Support multiple configuration patterns
- Preserve code formatting and comments
- Write modified code back to disk

## Technologies
- Tree-sitter parser (language-agnostic parsing)
- tree-sitter-javascript language binding
- S-expression based query language

## Key Operations
- `parse_javascript(source_code)` - Convert source to AST
- `query_ast(tree, query_string)` - Find nodes matching pattern
- `get_node_text(node)` - Extract source text from node
- `insert_text(file, position, text)` - Insert at byte offset
- `modify_object_property(node, property, value)` - Update object
- `write_file(path, content)` - Persist modified source

## Query Examples
- Find defineConfig calls: `(call_expression function: (identifier) @func)`
- Find object properties: `(pair key: (property_identifier) @key)`
- Locate export defaults: `(export_statement declaration: (object) @obj)`

## Supported Patterns
- `export default defineConfig({ ... })`
- `const config = { ... }; export default config;`
- `export default { ... }`
- `module.exports = { ... }`

## Precision
- Byte-exact positioning for insertions
- No regex fragility or false matches
- Handles nested structures and complex formatting
- Preserves whitespace and comments when possible

## Common Transformations
- Set vite.config.js base path for subdirectory deployment
- Inject Firebase configuration into config objects
- Update environment variables in .env files
- Add or modify webpack/build configurations

## Error Handling
- Malformed JavaScript syntax detection
- Missing expected AST nodes
- Query pattern matching failures
- File write permission errors

## Integration Points
- Used by Code Transformation Agent
- Processes vite.config.js files
- Handles firebase-config.js injection
- Supports multi-file modification

## Performance
- Linear time complexity for parsing
- Efficient tree traversal for queries
- Minimal memory overhead for large files
- No regex recompilation overhead

## Notes
- Safer than string replacement or regex
- Handles edge cases like optional chaining and nullish coalescing
- Language-aware syntax preservation
- Ideal for JavaScript configuration files
