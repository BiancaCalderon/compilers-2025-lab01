from SimpleLangParser import SimpleLangParser
from SimpleLangVisitor import SimpleLangVisitor
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckVisitor(SimpleLangVisitor):

  def visitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))
    op = ctx.op.text
    if op == '%':
      if not (isinstance(left_type, IntType) and isinstance(right_type, IntType)):
        raise TypeError("Unsupported operand types for %: {} and {}".format(left_type, right_type))
      return IntType()
    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
      if not (isinstance(left_type, BoolType) or isinstance(right_type, BoolType)):
        return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()
    raise TypeError("Unsupported operand types for {}: {} and {}".format(op, left_type, right_type))

  def visitAddSub(self, ctx: SimpleLangParser.AddSubContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))
    op = ctx.op.text
    if op == '+':
      if isinstance(left_type, StringType) or isinstance(right_type, StringType):
        if not (isinstance(left_type, StringType) and isinstance(right_type, StringType)):
          raise TypeError("Concatenation only allowed between strings: {} and {}".format(left_type, right_type))
        return StringType()
    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
      if not (isinstance(left_type, BoolType) or isinstance(right_type, BoolType)):
        return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()
    raise TypeError("Unsupported operand types for {}: {} and {}".format(op, left_type, right_type))

  def visitPow(self, ctx: SimpleLangParser.PowContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))
    if not (isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType))):
      raise TypeError("Unsupported operand types for ^: {} and {}".format(left_type, right_type))
    return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()

  def visitInt(self, ctx: SimpleLangParser.IntContext):
    return IntType()

  def visitFloat(self, ctx: SimpleLangParser.FloatContext):
    return FloatType()

  def visitString(self, ctx: SimpleLangParser.StringContext):
    return StringType()

  def visitBool(self, ctx: SimpleLangParser.BoolContext):
    return BoolType()

  def visitParens(self, ctx: SimpleLangParser.ParensContext):
    return self.visit(ctx.expr())
