#ifndef NODE_H
#define NODE_H

#include <string>
#include <vector>

class Node {
public:
    virtual ~Node() {}
    virtual void print() = 0;
};

class Statement : public Node {};

class Declaration : public Statement {
public:
    Declaration(std::string type, std::string identifier) : m_type(type), m_identifier(identifier) {}
    void print() override;

private:
    std::string m_type;
    std::string m_identifier;
};

class Assignment : public Statement {
public:
    Assignment(std::string identifier, Node *expression) : m_identifier(identifier), m_expression(expression) {}
    void print() override;

private:
    std::string m_identifier;
    Node *m_expression;
};

class Print : public Statement {
public:
    Print(Node *expression) : m_expression(expression) {}
    void print() override;

private:
    Node *m_expression;
};

class IfStatement : public Statement {
public:
    IfStatement(Node *condition, Node *thenBlock, Node *elseBlock = nullptr) : m_condition(condition), m_thenBlock(thenBlock), m_elseBlock(elseBlock) {}
    void print() override;

private:
    Node *m_condition;
    Node *m_thenBlock;
    Node *m_elseBlock;
};

class WhileLoop : public Statement {
public:
    WhileLoop(Node *condition, Node *block) : m_condition(condition), m_block(block) {}
    void print() override;

private:
    Node *m_condition;
    Node *m_block;
};

class ForLoop : public Statement {
public:
    ForLoop(Node *initialization, Node *condition, Node *increment, Node *block) : m_initialization(initialization), m_condition(condition),
                                                                                   m_increment(increment), m_block(block) {}
    void print() override;

private:
    Node *m_initialization;
    Node *m_condition;
    Node *m_increment;
    Node *m_block;
};

class FunctionDeclaration : public Statement {
public:
    FunctionDeclaration(std::string returnType, std::string identifier,
                        std::vector<std::pair<std::string, std::string>> parameters,
                        Node *block) : m_returnType(returnType), m_identifier(identifier),
                                       m_parameters(parameters), m_block(block) {}
    void print() override;

private:
    std::string m_returnType;
    std::string m_identifier;
    std::vector<std::pair<std::string, std::string>> m_parameters;
    Node *m_block;
};

class FunctionCall : public Node {
public:
    FunctionCall(std::string identifier, std::vector<Node *> arguments) : m_identifier(identifier), m_arguments(arguments) {}
    void print() override;

private:
    std::string m_identifier;
    std::vector<Node *> m_arguments;
};

class RelExpression : public Node {
public:
    RelExpression(Node *left, std::string op, Node *right) : m_left(left), m_op(op), m_right(right) {}
    void print() override;

private:
    Node *m_left;
    std::string m_op;
    Node *m_right;
};

class Expression : public Node {
public:
    Expression(Node *left, std::string op, Node *right) : m_left(left), m_op(op), m_right(right) {}
    void print() override;

private:
    Node *m_left;
    std::string m_op;
    Node *m_right;
};

class Term : public Node {
public:
    Term(Node *left, std::string op, Node *right) : m_left(left), m_op(op), m_right(right) {}
    void print()
