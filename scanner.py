import sys
import os
import clr

from System import String
from System.IO import File
from System.Collections.Generic import List
from Microsoft.CodeAnalysis import SyntaxTree
from Microsoft.CodeAnalysis.CSharp import CSharpSyntaxTree
from Microsoft.CodeAnalysis.CSharp.Syntax import *

def load_assemblies():
    assemblies_path = r'./assemblies/'
    clr.AddReference(os.path.join(assemblies_path, 'Microsoft.CodeAnalysis.dll'))
    clr.AddReference(os.path.join(assemblies_path, 'Microsoft.CodeAnalysis.CSharp.dll'))

def scan_code(code):
    tree = CSharpSyntaxTree.ParseText(code)
    root = tree.GetRoot()

    vulnerabilities = []

    vulnerabilities.extend(check_for_hardcoded_passwords(root))
    vulnerabilities.extend(check_for_sql_injection(root))
    vulnerabilities.extend(check_for_insecure_crypto_algorithms(root))

    return vulnerabilities

def check_for_hardcoded_passwords(root):
    vulnerabilities = []
    variable_declarations = root.DescendantNodes().OfType(VariableDeclaratorSyntax)
    for variable in variable_declarations:
        name = variable.Identifier.Text
        if 'password' in name.lower():
            initializer = variable.Initializer
            if initializer:
                value = initializer.Value
                if isinstance(value, LiteralExpressionSyntax) and value.IsKind(SyntaxKind.StringLiteralExpression):
                    line = variable.GetLocation().GetLineSpan().StartLinePosition.Line + 1
                    vulnerabilities.append(f"Hardcoded password found in variable '{name}' at line {line}.")
    return vulnerabilities

def check_for_sql_injection(root):
    vulnerabilities = []
    invocations = root.DescendantNodes().OfType(InvocationExpressionSyntax)
    for invocation in invocations:
        expression = invocation.Expression
        if isinstance(expression, MemberAccessExpressionSyntax):
            method_name = expression.Name.Identifier.Text
            if method_name.lower() in ['executequery', 'executenonquery', 'executereader']:
                arguments = invocation.ArgumentList.Arguments
                for arg in arguments:
                    if isinstance(arg.Expression, BinaryExpressionSyntax) and arg.Expression.IsKind(SyntaxKind.AddExpression):
                        line = invocation.GetLocation().GetLineSpan().StartLinePosition.Line + 1
                        vulnerabilities.append(f"Possible SQL Injection vulnerability at line {line}.")
    return vulnerabilities

def check_for_insecure_crypto_algorithms(root):
    vulnerabilities = []
    object_creations = root.DescendantNodes().OfType(ObjectCreationExpressionSyntax)
    for creation in object_creations:
        type_str = creation.Type.ToString()
        if 'MD5' in type_str or 'SHA1' in type_str:
            line = creation.GetLocation().GetLineSpan().StartLinePosition.Line + 1
            vulnerabilities.append(f"Use of insecure cryptographic algorithm '{type_str}' at line {line}.")
    return vulnerabilities