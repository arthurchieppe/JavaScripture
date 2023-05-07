#include <iostream>
#include <vector>
#include <llvm/Value.h>

class CodeGenContext;

class Node {
public:
    virtual ~Node() {}
    virtual llvm::Value* codeGen(CodeGenContext& context) { }
};

class NExpression : public Node {
};

class NStatement : public Node {
};

class NInteger : public NExpression {
public:
    long long value;
    NInteger(long long value) : value(value) { }
    virtual llvm::Value* codeGen(CodeGenContext& context);
};

class NDouble : public NExpression {
public:
    double value;
    NDouble(double value) : value(value) { }
    virtual llvm::Value* codeGen(CodeGenContext& context);
};

class NIdentifier : public NExpression {
public:
    std::string name;
    NIdentifier(const std::string& name) : name(name) { }
    virtual llvm::Value* codeGen(CodeGenContext& context);
};

class NMethodCall : public NExpression {
public:
    const NIdentifier& id;
    std::vector<NExpression*> arguments;
    NMethodCall(const NIdentifier& id, std::vector<NExpression*>& arguments) :
        id(id), arguments(arguments) { }
    NMethodCall(const NIdentifier& id) : id(id) { }
    virtual llvm::Value* codeGen(CodeGenContext& context);
};

class NBinaryOperator : public NExpression {
public:
    int op;
    NExpression& lhs;
    NExpression& rhs;
    NBinaryOperator(NExpression& lhs, int op, NExpression& rhs) :
        lhs(lhs), rhs(rhs), op(op) { }
    virtual llvm::Value* codeGen(CodeGenContext& context);
};

class NUnaryOperator : public NExpression {
public:
    int op;
    NExpression& operand;
    NUnaryOperator(int op, NExpression& operand) :
        op(op), operand(operand) { }
    virtual llvm::Value* codeGen(CodeGenContext& context);
};

class NAssignment : public NExpression {
public:
    NIdentifier& lhs;
    NExpression& rhs;
    NAssignment(NIdentifier& lhs, NExpression& rhs) :
        lhs(lhs), rhs(rhs) { }
    virtual llvm::Value* codeGen(CodeGenContext& context);
};

class NPrintStatement : public NStatement {
public:
    NExpression& expression;
    NPrintStatement(NExpression& expression) :
        expression(expression) { }
    virtual llvm::Value* codeGen(CodeGenContext& context);
};

class NDeclaration : public NStatement {
public:
    const NIdentifier& type;
    NIdentifier& id;
    NDeclaration(const NIdentifier& type, NIdentifier& id) :
        type(type), id(id) { }
    virtual llvm::Value* codeGen(CodeGenContext& context);
};

class NWhileStatement : public NStatement {
public:
    NExpression& condition;
    NBlock& block;
    NWhileStatement(NExpression& condition, NBlock& block) :
        condition(condition), block(block) { }
    virtual llvm::Value* codeGen(CodeGenContext& context);
};

class NForStatement : public NStatement {
public:
    NExpression& init;
    NExpression& condition;
    NExpression& increment;
    NBlock& block;
    NForStatement(NExpression& init, NExpression& condition,
        NExpression& increment, NBlock& block) :
        init(init), condition(condition), increment(increment), block(block) { }
    virtual llvm::Value* codeGen(CodeGenContext& context);
};

class NIfStatement : public NStatement {
public:
    NExpression& condition;
    NBlock& ifBlock;
    NBlock* elseBlock;
    NIfStatement(NExpression& condition, NBlock& ifBlock, NBlock* elseBlock = nullptr) :
        condition(condition), ifBlock(ifBlock), elseBlock(elseBlock) { }
    virtual llvm::Value* codeGen(CodeGenContext& context);
};

class NReturnStatement : public NStatement {
public:
    NExpression& expression;
    NReturnStatement(NExpression& expression) :
        expression(expression) { }
    virtual llvm::Value* codeGen(CodeGenContext& context);
};