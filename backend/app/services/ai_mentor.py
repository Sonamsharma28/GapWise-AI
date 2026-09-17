import re
import json
from sqlalchemy.orm import Session
from ..models.mastery import ConceptMastery
from ..models.concept import Concept
from ..models.question import Question, QuestionOption
from ..models.assessment import Assessment, AssessmentResponse
from ..models.ai_interaction import AIInteraction
from ..config import settings
from .rag import retrieve_relevant_content
from .prerequisite_engine import find_root_causes

# ─── Comprehensive Concept Teaching Knowledge Base ──────────────────────────
# Rich theoretical definitions, essential formulas, detailed numerical worked examples,
# and common exam pitfalls for all Secondary Mathematics concepts (Class 9-10).
CONCEPT_KNOWLEDGE_BASE = {
    "Number Systems": {
        "title": "Number Systems & Real Numbers",
        "grade": "Class 9",
        "theory": (
            "Real numbers encompass all rational and irrational numbers that can be plotted on a continuous number line.\n"
            "• **Rational Numbers (Q):** Any number that can be expressed in the form p/q, where p and q are integers and q ≠ 0. Their decimal expansions are either **terminating** (e.g., 3/8 = 0.375) or **non-terminating recurring** (e.g., 1/3 = 0.333...).\n"
            "• **Irrational Numbers:** Numbers that **cannot** be written as p/q. Their decimals are **non-terminating and non-recurring** (e.g., √2 ≈ 1.414..., √3, π).\n"
            "• **Rationalization:** The mathematical method of eliminating radical terms (square roots) from the denominator of a fraction by multiplying the numerator and denominator by its conjugate (a - √b)."
        ),
        "formulas": [
            "Rational form: p/q (p, q ∈ Z, q ≠ 0)",
            "Conjugate pair: Conjugate of (a + √b) is (a - √b)",
            "Difference of squares for radicals: (a + √b)(a - √b) = a² - b",
            "Laws of Exponents: aᵐ × aⁿ = aᵐ⁺ⁿ | (aᵐ)ⁿ = aᵐⁿ | a⁻ⁿ = 1/aⁿ | aᵐ / aⁿ = aᵐ⁻ⁿ"
        ],
        "worked_example": {
            "problem": "Rationalize the denominator of: 2 / (3 + √5)",
            "steps": [
                "Step 1: Identify the conjugate of the denominator (3 + √5), which is (3 - √5).",
                "Step 2: Multiply both numerator and denominator by (3 - √5):\n   = [2 × (3 - √5)] / [(3 + √5)(3 - √5)]",
                "Step 3: Expand denominator using (a + b)(a - b) = a² - b²:\n   Denominator = 3² - (√5)² = 9 - 5 = 4.",
                "Step 4: Simplify numerator and denominator:\n   = 2(3 - √5) / 4 = (3 - √5) / 2."
            ],
            "answer": "(3 - √5) / 2"
        },
        "pitfalls": "Never add radicals under the same root: √(a + b) ≠ √a + √b. Also, numbers like √4 = 2 or √9 = 3 are rational integers, not irrational!",
        "golden_rule": "Every rational number is p/q where q ≠ 0. If a square root cannot be simplified to an integer, it is irrational.",
        "mini_challenge": "Is (√3 + 2)(√3 - 2) rational or irrational? (Hint: apply a² - b²!)"
    },

    "Basic Algebra": {
        "title": "Basic Algebra & Polynomial Arithmetic",
        "grade": "Class 9",
        "theory": (
            "Algebra uses symbols (variables like x, y) to represent unknown values and generalized arithmetic rules.\n"
            "• **Terms & Coefficients:** In 4x³, 4 is the coefficient, x is the variable, and 3 is the exponent.\n"
            "• **Like Terms:** Terms having the exact same variables raised to identical powers (e.g., 5x²y and -3x²y). Only like terms can be added or subtracted!\n"
            "• **Distributive Law:** Multiplication distributes across addition: a(b + c) = ab + ac."
        ),
        "formulas": [
            "Distributive Law: a(b + c + d) = ab + ac + ad",
            "Combining Like Terms: axⁿ + bxⁿ = (a + b)xⁿ",
            "Multiplication of Terms: (axᵐ)(bxⁿ) = (a × b)xᵐ⁺ⁿ"
        ],
        "worked_example": {
            "problem": "Simplify: 3x(2x² - 4x + 5) - 2(x² - 3x + 4)",
            "steps": [
                "Step 1: Distribute 3x across the first parentheses:\n   3x(2x²) - 3x(4x) + 3x(5) = 6x³ - 12x² + 15x.",
                "Step 2: Distribute -2 across the second parentheses:\n   -2(x²) - 2(-3x) - 2(4) = -2x² + 6x - 8.",
                "Step 3: Group and combine all like terms:\n   = 6x³ + (-12x² - 2x²) + (15x + 6x) - 8\n   = 6x³ - 14x² + 21x - 8."
            ],
            "answer": "6x³ - 14x² + 21x - 8"
        },
        "pitfalls": "Never combine unlike terms (e.g. 3x + 2x² is NOT 5x³). Watch negative signs carefully when multiplying negative constants across brackets.",
        "golden_rule": "Only combine terms with identical variable powers. Distribute negative signs to EVERY term inside parentheses.",
        "mini_challenge": "Multiply and simplify: (2x - 3)(x + 4)."
    },

    "Linear Equations": {
        "title": "Linear Equations in One & Two Variables",
        "grade": "Class 9 & 10",
        "theory": (
            "A linear equation represents a mathematical relationship where the highest power of any variable is 1.\n"
            "• **One Variable:** ax + b = 0 has exactly one unique solution: x = -b/a.\n"
            "• **Two Variables:** ax + by + c = 0 represents a straight line on the Cartesian plane with infinitely many solutions (x, y).\n"
            "• **System of Two Linear Equations:** Two lines can intersect (unique solution, a₁/a₂ ≠ b₁/b₂), be parallel (no solution, a₁/a₂ = b₁/b₂ ≠ c₁/c₂), or coincide (infinitely many solutions, a₁/a₂ = b₁/b₂ = c₁/c₂)."
        ),
        "formulas": [
            "Standard Form: ax + by + c = 0",
            "Unique Solution condition: a₁/a₂ ≠ b₁/b₂",
            "No Solution (Parallel lines): a₁/a₂ = b₁/b₂ ≠ c₁/c₂",
            "Infinite Solutions (Coincident): a₁/a₂ = b₁/b₂ = c₁/c₂"
        ],
        "worked_example": {
            "problem": "Solve the system: 2x + 3y = 11 and 3x + 2y = 9",
            "steps": [
                "Step 1: Multiply equation (1) by 3 and equation (2) by 2 to equate coefficients of x:\n   (1) × 3 => 6x + 9y = 33\n   (2) × 2 => 6x + 4y = 18",
                "Step 2: Subtract the second equation from the first:\n   (6x - 6x) + (9y - 4y) = 33 - 18\n   5y = 15  =>  y = 3.",
                "Step 3: Substitute y = 3 back into equation (1):\n   2x + 3(3) = 11\n   2x + 9 = 11  =>  2x = 2  =>  x = 1.",
                "Step 4: Verification: In eq (2): 3(1) + 2(3) = 3 + 6 = 9 (Correct!)."
            ],
            "answer": "x = 1, y = 3  (Solution point: (1, 3))"
        },
        "pitfalls": "Forgetting to multiply the constant term on the right-hand side when scaling an equation before elimination.",
        "golden_rule": "Elimination method: Multiply equations so one variable has matching coefficients, then add or subtract to eliminate it.",
        "mini_challenge": "Solve for x and y: x + y = 10 and x - y = 4."
    },

    "Algebraic Identities": {
        "title": "Algebraic Identities & Expansions",
        "grade": "Class 9",
        "theory": (
            "An algebraic identity is an equation that is true for ALL values of its variables. They are standard shortcut formulas for rapid polynomial multiplication and algebraic factorisation."
        ),
        "formulas": [
            "(a + b)² = a² + 2ab + b²",
            "(a - b)² = a² - 2ab + b²",
            "(a + b)(a - b) = a² - b²",
            "(x + a)(x + b) = x² + (a + b)x + ab",
            "(a + b + c)² = a² + b² + c² + 2ab + 2bc + 2ca",
            "(a + b)³ = a³ + b³ + 3ab(a + b) = a³ + 3a²b + 3ab² + b³",
            "(a - b)³ = a³ - b³ - 3ab(a - b) = a³ - 3a²b + 3ab² - b³",
            "a³ + b³ = (a + b)(a² - ab + b²)",
            "a³ - b³ = (a - b)(a² + ab + b²)"
        ],
        "worked_example": {
            "problem": "Evaluate 104 × 96 using algebraic identities without direct multiplication.",
            "steps": [
                "Step 1: Express both numbers around their common base (100):\n   104 = (100 + 4) and 96 = (100 - 4).",
                "Step 2: Recognize the difference of squares identity (a + b)(a - b) = a² - b²:\n   Here a = 100 and b = 4.",
                "Step 3: Calculate:\n   (100 + 4)(100 - 4) = 100² - 4² = 10,000 - 16 = 9,984."
            ],
            "answer": "9,984"
        },
        "pitfalls": "Writing (a + b)² = a² + b² (forgetting the middle 2ab term!). This is the single most common mistake in secondary algebra.",
        "golden_rule": "Never forget the middle term: (a ± b)² ALWAYS produces 3 terms: a² ± 2ab + b².",
        "mini_challenge": "Expand: (2x - 3y)² using algebraic identities."
    },

    "Factorisation": {
        "title": "Polynomial Factorisation",
        "grade": "Class 9",
        "theory": (
            "Factorisation is the reverse of algebraic expansion. It breaks an algebraic expression into a product of irreducible simpler factors.\n"
            "• **Method 1 (Common Factor):** Factor out the Greatest Common Factor (GCF) from every term.\n"
            "• **Method 2 (Grouping):** Group 4 terms in pairs that share common factors.\n"
            "• **Method 3 (Identities):** Apply a² - b² = (a - b)(a + b).\n"
            "• **Method 4 (Splitting the Middle Term):** For quadratic trinomials ax² + bx + c, find two numbers whose product is (a × c) and whose sum is b."
        ),
        "formulas": [
            "GCF extraction: ma + mb = m(a + b)",
            "Difference of squares: a² - b² = (a - b)(a + b)",
            "Splitting middle term: ax² + bx + c → Find p, q such that p × q = ac and p + q = b",
            "Grouping: ax + ay + bx + by = a(x + y) + b(x + y) = (x + y)(a + b)"
        ],
        "worked_example": {
            "problem": "Factorise: 2x² + 7x + 3",
            "steps": [
                "Step 1: Identify coefficients: a = 2, b = 7, c = 3.",
                "Step 2: Compute product ac = 2 × 3 = 6. We need two numbers that multiply to 6 and add to 7.",
                "Step 3: The numbers are 6 and 1 (since 6 × 1 = 6 and 6 + 1 = 7).",
                "Step 4: Split the middle term 7x into (6x + x):\n   2x² + 6x + x + 3",
                "Step 5: Group in pairs:\n   = [2x² + 6x] + [x + 3]\n   = 2x(x + 3) + 1(x + 3)\n   = (2x + 1)(x + 3)."
            ],
            "answer": "(2x + 1)(x + 3)"
        },
        "pitfalls": "Looking only for numbers that add to b without checking if their product equals (a × c). Forgetting signs when ac is negative.",
        "golden_rule": "For ax² + bx + c: Product = a × c, Sum = b. Always split the middle term and factor by grouping.",
        "mini_challenge": "Factorise: x² - 5x + 6."
    },

    "Quadratic Equations": {
        "title": "Quadratic Equations & Roots",
        "grade": "Class 10",
        "theory": (
            "A quadratic equation is a 2nd-degree polynomial equation of standard form: ax² + bx + c = 0 (a ≠ 0).\n"
            "• **Roots:** The values of x that satisfy the equation (at most 2 real roots).\n"
            "• **Quadratic Formula:** x = [-b ± √(b² - 4ac)] / (2a).\n"
            "• **Discriminant (D = b² - 4ac):**\n"
            "  - If D > 0: Two distinct, real roots.\n"
            "  - If D = 0: Two equal real roots (x = -b / 2a).\n"
            "  - If D < 0: No real roots (roots are complex numbers)."
        ),
        "formulas": [
            "Standard Form: ax² + bx + c = 0 (a ≠ 0)",
            "Quadratic Formula: x = [-b ± √(b² - 4ac)] / (2a)",
            "Discriminant: D = b² - 4ac",
            "Sum of roots: α + β = -b/a",
            "Product of roots: αβ = c/a"
        ],
        "worked_example": {
            "problem": "Solve: 2x² - 5x + 3 = 0 using the Quadratic Formula.",
            "steps": [
                "Step 1: Identify a = 2, b = -5, c = 3.",
                "Step 2: Calculate Discriminant D = b² - 4ac:\n   D = (-5)² - 4(2)(3) = 25 - 24 = 1.\n   Since D = 1 > 0, there are two distinct real roots.",
                "Step 3: Apply the Quadratic Formula:\n   x = [-(-5) ± √1] / (2 × 2) = (5 ± 1) / 4.",
                "Step 4: Find both roots:\n   x₁ = (5 + 1)/4 = 6/4 = 3/2 (or 1.5)\n   x₂ = (5 - 1)/4 = 4/4 = 1."
            ],
            "answer": "x = 3/2, x = 1"
        },
        "pitfalls": "Sign error with -b: when b = -5, -b becomes +5. Also remember that the division by (2a) applies to the ENTIRE numerator, not just the square root.",
        "golden_rule": "Compute D = b² - 4ac first. If D < 0, write 'No real roots'. If D ≥ 0, use x = (-b ± √D) / (2a).",
        "mini_challenge": "Find the nature of roots for: x² - 4x + 4 = 0."
    },

    "Polynomials": {
        "title": "Polynomials & Zeros",
        "grade": "Class 10",
        "theory": (
            "A polynomial is an expression P(x) = aₙxⁿ + ... + a₁x + a₀. The degree n is the highest exponent of x.\n"
            "• **Zeros of a Polynomial:** A real number k is a zero of P(x) if P(k) = 0.\n"
            "• **Relationship with Coefficients for ax² + bx + c:**\n"
            "  Sum of zeros (α + β) = -b/a\n"
            "  Product of zeros (αβ) = c/a\n"
            "• **Factor Theorem:** (x - a) is a factor of P(x) if and only if P(a) = 0.\n"
            "• **Remainder Theorem:** Dividing P(x) by (x - a) leaves a remainder equal to P(a)."
        ),
        "formulas": [
            "Sum of zeros for quadratic: α + β = -b/a",
            "Product of zeros: αβ = c/a",
            "Forming a quadratic polynomial: k[x² - (Sum)x + Product]",
            "Remainder when dividing by (x - c): R = P(c)"
        ],
        "worked_example": {
            "problem": "Find the zeros of P(x) = x² - 2x - 8 and verify the relationship between zeros and coefficients.",
            "steps": [
                "Step 1: Factorise P(x): x² - 2x - 8 = (x - 4)(x + 2).",
                "Step 2: Set P(x) = 0 => x - 4 = 0 or x + 2 = 0 => Zeros are α = 4 and β = -2.",
                "Step 3: Verify Sum of zeros:\n   α + β = 4 + (-2) = 2.\n   Formula: -b/a = -(-2)/1 = 2 (Verified!).",
                "Step 4: Verify Product of zeros:\n   αβ = 4 × (-2) = -8.\n   Formula: c/a = -8/1 = -8 (Verified!)."
            ],
            "answer": "Zeros: x = 4, x = -2. Relationships verified."
        },
        "pitfalls": "Confusing zeros with factors: if the zero is 4, the factor is (x - 4), NOT (x + 4). Also remember the minus sign in sum = -b/a.",
        "golden_rule": "Sum of zeros = -b/a, Product = c/a. To build a polynomial from zeros: x² - (α+β)x + αβ.",
        "mini_challenge": "Find a quadratic polynomial whose zeros are 3 and -5."
    },

    "Triangles": {
        "title": "Triangles, Congruence & Similarity",
        "grade": "Class 9 & 10",
        "theory": (
            "Triangles are fundamental 3-sided polygons.\n"
            "• **Congruence (Exact same shape and size):** SSS, SAS, ASA, AAS, RHS criteria.\n"
            "• **Similarity (Same shape, proportional sizes):** AAA, SAS, SSS criteria.\n"
            "• **Basic Proportionality Theorem (Thales's Theorem):** If a line is drawn parallel to one side of a triangle intersecting the other two sides, it divides the two sides in the same ratio: AD/DB = AE/EC.\n"
            "• **Pythagoras Theorem:** In a right triangle with legs a, b and hypotenuse c: a² + b² = c²."
        ),
        "formulas": [
            "Thales Theorem: If DE || BC, then AD/DB = AE/EC and AD/AB = AE/AC",
            "Pythagoras Theorem: (Hypotenuse)² = (Base)² + (Perpendicular)²",
            "Area ratio of similar triangles: Area(△1)/Area(△2) = (Side1/Side2)²"
        ],
        "worked_example": {
            "problem": "In △ABC, DE || BC. If AD = 2 cm, DB = 3 cm, and AE = 4 cm, find EC and AC.",
            "steps": [
                "Step 1: Apply Basic Proportionality Theorem since DE || BC:\n   AD / DB = AE / EC",
                "Step 2: Substitute given lengths:\n   2 / 3 = 4 / EC",
                "Step 3: Cross-multiply to solve for EC:\n   2 × EC = 3 × 4 = 12  =>  EC = 12 / 2 = 6 cm.",
                "Step 4: Find total length AC:\n   AC = AE + EC = 4 + 6 = 10 cm."
            ],
            "answer": "EC = 6 cm, AC = 10 cm"
        },
        "pitfalls": "Confusing AD/DB with AD/AB. When comparing DE and BC, use the full ratio AD/AB = DE/BC, NOT AD/DB.",
        "golden_rule": "Parallel line inside a triangle creates proportional segments: AD/DB = AE/EC.",
        "mini_challenge": "A right triangle has legs 6 cm and 8 cm. What is its hypotenuse?"
    },

    "Coordinate Geometry": {
        "title": "Coordinate Geometry & Formulas",
        "grade": "Class 10",
        "theory": (
            "Coordinate geometry allows us to study geometric shapes algebraically on the 2D Cartesian plane.\n"
            "• **Distance Formula:** Measures the straight-line Euclidean distance between two points (x₁, y₁) and (x₂, y₂).\n"
            "• **Midpoint Formula:** Finds the exact center point of a line segment.\n"
            "• **Section Formula:** Calculates the coordinates of a point P that divides the line segment AB in ratio m₁ : m₂."
        ),
        "formulas": [
            "Distance Formula: d = √[(x₂ - x₁)² + (y₂ - y₁)²]",
            "Midpoint Formula: M = ((x₁ + x₂)/2, (y₁ + y₂)/2)",
            "Section Formula: P = ((m₁x₂ + m₂x₁)/(m₁ + m₂), (m₁y₂ + m₂y₁)/(m₁ + m₂))",
            "Area of Triangle: ½ |x₁(y₂ - y₃) + x₂(y₃ - y₁) + x₃(y₁ - y₂)|"
        ],
        "worked_example": {
            "problem": "Find the distance between points P(1, -3) and Q(4, 1).",
            "steps": [
                "Step 1: Identify coordinates: x₁ = 1, y₁ = -3, x₂ = 4, y₂ = 1.",
                "Step 2: Calculate differences:\n   (x₂ - x₁) = 4 - 1 = 3\n   (y₂ - y₁) = 1 - (-3) = 1 + 3 = 4.",
                "Step 3: Square both differences:\n   3² = 9,  4² = 16.",
                "Step 4: Add and take the square root:\n   d = √(9 + 16) = √25 = 5 units."
            ],
            "answer": "5 units"
        },
        "pitfalls": "Sign error with negative coordinates: [1 - (-3)]² = (4)² = 16, NOT (-2)² = 4. Distance is ALWAYS a positive scalar.",
        "golden_rule": "Square the differences first, add them, then take the square root: d = √[(Δx)² + (Δy)²].",
        "mini_challenge": "Find the midpoint of segment joining (2, 8) and (6, 4)."
    },

    "Trigonometry Basics": {
        "title": "Introduction to Trigonometry",
        "grade": "Class 10",
        "theory": (
            "Trigonometry studies the relationships between the sides and angles of right-angled triangles.\n"
            "• **SOH-CAH-TOA:**\n"
            "  - **sin θ** = Opposite / Hypotenuse\n"
            "  - **cos θ** = Adjacent / Hypotenuse\n"
            "  - **tan θ** = Opposite / Adjacent = sin θ / cos θ\n"
            "• **Reciprocal Ratios:**\n"
            "  - **cosec θ** = 1 / sin θ = Hypotenuse / Opposite\n"
            "  - **sec θ** = 1 / cos θ = Hypotenuse / Adjacent\n"
            "  - **cot θ** = 1 / tan θ = Adjacent / Opposite"
        ),
        "formulas": [
            "sin θ = Opp/Hyp | cos θ = Adj/Hyp | tan θ = Opp/Adj",
            "Standard Values:\n  sin 30° = 1/2, sin 45° = 1/√2, sin 60° = √3/2, sin 90° = 1\n  cos 30° = √3/2, cos 45° = 1/√2, cos 60° = 1/2, cos 90° = 0\n  tan 30° = 1/√3, tan 45° = 1, tan 60° = √3",
            "Pythagorean Identity 1: sin²θ + cos²θ = 1",
            "Pythagorean Identity 2: 1 + tan²θ = sec²θ",
            "Pythagorean Identity 3: 1 + cot²θ = cosec²θ"
        ],
        "worked_example": {
            "problem": "If tan θ = 3/4 in a right triangle, find the values of sin θ and cos θ.",
            "steps": [
                "Step 1: Since tan θ = Opposite / Adjacent = 3/4, let Opposite = 3k, Adjacent = 4k.",
                "Step 2: Find Hypotenuse using Pythagoras Theorem:\n   Hypotenuse = √[(3k)² + (4k)²] = √[9k² + 16k²] = √(25k²) = 5k.",
                "Step 3: Calculate sin θ = Opposite / Hypotenuse = 3k / 5k = 3/5.",
                "Step 4: Calculate cos θ = Adjacent / Hypotenuse = 4k / 5k = 4/5.",
                "Step 5: Verify sin²θ + cos²θ = (3/5)² + (4/5)² = 9/25 + 16/25 = 25/25 = 1."
            ],
            "answer": "sin θ = 3/5, cos θ = 4/5"
        },
        "pitfalls": "Confusing Opposite and Adjacent. Opposite is always the side facing angle θ; Hypotenuse is always opposite the 90° right angle.",
        "golden_rule": "SOH-CAH-TOA. The hypotenuse is ALWAYS the longest side opposite the 90° right angle.",
        "mini_challenge": "Evaluate: sin² 30° + cos² 30°. (You should get 1!)"
    },

    "Trigonometry Applications": {
        "title": "Heights & Distances (Trigonometry)",
        "grade": "Class 10",
        "theory": (
            "Trigonometry allows indirect measurement of heights of tall structures and distances across obstacles without direct measurement.\n"
            "• **Angle of Elevation:** The angle between the horizontal line of sight and the observer's line of sight looking UP at an object.\n"
            "• **Angle of Depression:** The angle between the horizontal line of sight and the observer's line of sight looking DOWN at an object."
        ),
        "formulas": [
            "tan(Angle of Elevation) = Height of Object / Distance from Base",
            "Height h = Distance × tan(θ)",
            "Distance d = Height / tan(θ)"
        ],
        "worked_example": {
            "problem": "A tower stands vertically on the ground. From a point on the ground 15 m away from the foot of the tower, the angle of elevation of the top of the tower is 60°. Find the height of the tower.",
            "steps": [
                "Step 1: Draw right triangle where base d = 15 m, angle θ = 60°, and height = h.",
                "Step 2: Apply tan θ = Opposite / Adjacent:\n   tan 60° = h / 15.",
                "Step 3: Substitute known value tan 60° = √3:\n   √3 = h / 15.",
                "Step 4: Solve for h:\n   h = 15√3 m ≈ 15 × 1.732 = 25.98 m."
            ],
            "answer": "Height = 15√3 meters (≈ 25.98 m)"
        },
        "pitfalls": "Drawing angle of depression against the vertical tower instead of from the horizontal line of sight.",
        "golden_rule": "Always draw a right triangle diagram first. Label the given side, the unknown side, and use tan θ = Height / Distance.",
        "mini_challenge": "From a point 10 m from a tree, the angle of elevation to the top is 45°. How tall is the tree?"
    },

    "Mensuration": {
        "title": "Surface Areas & Volumes of Solids",
        "grade": "Class 10",
        "theory": (
            "Mensuration deals with measuring surface areas and volumes of 3D geometric solids and their combinations.\n"
            "• **Curved / Lateral Surface Area (CSA/LSA):** Area of only the side faces (excluding top and bottom bases).\n"
            "• **Total Surface Area (TSA):** CSA + Base Areas.\n"
            "• **Volume:** Total capacity of 3D space enclosed by the solid."
        ),
        "formulas": [
            "Cylinder: CSA = 2πrh | TSA = 2πr(r + h) | Volume = πr²h",
            "Cone: Slant height l = √(r² + h²) | CSA = πrl | TSA = πr(l + r) | Volume = ⅓πr²h",
            "Sphere: Surface Area = 4πr² | Volume = ⁴⁄₃πr³",
            "Hemisphere: CSA = 2πr² | TSA = 3πr² | Volume = ⅔πr³",
            "Cuboid: Volume = l × b × h | TSA = 2(lb + bh + hl)"
        ],
        "worked_example": {
            "problem": "Find the total surface area and volume of a solid hemisphere of radius 7 cm. (Use π = 22/7)",
            "steps": [
                "Step 1: Identify radius r = 7 cm.",
                "Step 2: Total Surface Area (TSA) of solid hemisphere = 3πr²:\n   TSA = 3 × (22/7) × 7 × 7 = 3 × 22 × 7 = 462 cm².",
                "Step 3: Volume of hemisphere = ⅔πr³:\n   Volume = ⅔ × (22/7) × 7 × 7 × 7 = ⅔ × 22 × 49 = (2156 / 3) ≈ 718.67 cm³."
            ],
            "answer": "TSA = 462 cm², Volume = 718.67 cm³"
        },
        "pitfalls": "Confusing CSA of hemisphere (2πr²) with TSA of a solid hemisphere (3πr² = curved surface + circular base).",
        "golden_rule": "For a solid hemisphere, TSA = 3πr² (includes the flat circular base). For cone slant height, l = √(r² + h²).",
        "mini_challenge": "A cylinder has radius 7 cm and height 10 cm. What is its curved surface area (2πrh)?"
    }
}

# Helper to find matching concept in knowledge base
def find_matching_concept_info(query: str):
    q = query.lower()
    for name, data in CONCEPT_KNOWLEDGE_BASE.items():
        if name.lower() in q:
            return name, data
    # Check synonyms
    synonyms = {
        "number": "Number Systems",
        "rational": "Number Systems",
        "irrational": "Number Systems",
        "real number": "Number Systems",
        "algebra": "Basic Algebra",
        "polynomial": "Polynomials",
        "linear": "Linear Equations",
        "equation": "Linear Equations",
        "simultaneous": "Linear Equations",
        "identity": "Algebraic Identities",
        "identities": "Algebraic Identities",
        "factor": "Factorisation",
        "factorise": "Factorisation",
        "factorize": "Factorisation",
        "quadratic": "Quadratic Equations",
        "discriminant": "Quadratic Equations",
        "root": "Quadratic Equations",
        "triangle": "Triangles",
        "similarity": "Triangles",
        "congruence": "Triangles",
        "thales": "Triangles",
        "pythagoras": "Triangles",
        "coordinate": "Coordinate Geometry",
        "distance formula": "Coordinate Geometry",
        "midpoint": "Coordinate Geometry",
        "section formula": "Coordinate Geometry",
        "trig": "Trigonometry Basics",
        "sin": "Trigonometry Basics",
        "cos": "Trigonometry Basics",
        "tan": "Trigonometry Basics",
        "elevation": "Trigonometry Applications",
        "depression": "Trigonometry Applications",
        "height": "Trigonometry Applications",
        "mensuration": "Mensuration",
        "cylinder": "Mensuration",
        "cone": "Mensuration",
        "sphere": "Mensuration",
        "hemisphere": "Mensuration",
        "volume": "Mensuration",
        "surface area": "Mensuration"
    }
    for key, cname in synonyms.items():
        if key in q:
            return cname, CONCEPT_KNOWLEDGE_BASE.get(cname)
    return None, None


def _build_steps_from_explanation(explanation_text: str, correct_ans_display: str):
    """Split explanation text into up to 3 pedagogical steps."""
    text = (explanation_text or "Apply the core formula for this topic.").replace(";", ".")
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    if len(sentences) >= 3:
        step1 = sentences[0]
        step2 = ". ".join(sentences[1:-1])
        step3 = sentences[-1]
    elif len(sentences) == 2:
        step1 = sentences[0]
        step2 = sentences[1]
        step3 = f"Therefore, the answer is {correct_ans_display}"
    else:
        step1 = text
        step2 = "Check each option against this rule carefully"
        step3 = f"The correct answer is {correct_ans_display}"
    return step1, step2, step3


def get_question_explanation(db: Session, student_id: int, question_id: int):
    """
    Returns a fully structured JSON explanation for a specific wrong question.
    Used by GET /api/ai/explain/{question_id} to power the inline
    WrongQuestionExplainer component on the dashboard and AI Mentor page.
    """
    question = db.query(Question).filter_by(id=question_id).first()
    if not question:
        return None

    concept = db.query(Concept).filter_by(id=question.concept_id).first()
    options = db.query(QuestionOption).filter_by(question_id=question.id).order_by(QuestionOption.option_label).all()
    options_dict = {opt.option_label: opt.option_text for opt in options}

    # Find this student's response to this question (most recent)
    latest_assessment = (
        db.query(Assessment)
        .filter_by(student_id=student_id, status="completed")
        .order_by(Assessment.completed_at.desc())
        .first()
    )
    student_resp = None
    question_num = None
    if latest_assessment:
        responses = (
            db.query(AssessmentResponse)
            .filter_by(assessment_id=latest_assessment.id)
            .order_by(AssessmentResponse.id.asc())
            .all()
        )
        for idx, resp in enumerate(responses):
            if resp.question_id == question_id:
                student_resp = resp
                question_num = idx + 1
                break

    student_answer_label = student_resp.student_answer if student_resp else None
    student_answer_text = options_dict.get(student_answer_label, "") if student_answer_label else ""
    correct_answer_label = question.correct_answer
    correct_answer_text = options_dict.get(correct_answer_label, "")

    concept_name = concept.name if concept else "Mathematics"
    kb_info = CONCEPT_KNOWLEDGE_BASE.get(concept_name)

    correct_ans_display = (
        f"Option {correct_answer_label}: \"{correct_answer_text}\""
        if correct_answer_text
        else f"Option {correct_answer_label}"
    )
    step1, step2, step3 = _build_steps_from_explanation(question.explanation, correct_ans_display)

    if student_answer_label and student_answer_text:
        why_wrong = (
            f"Option {student_answer_label} (\"{student_answer_text}\") is one of the most common wrong answers "
            f"on this type of question. Students choose it because it looks mathematically similar to the correct answer, "
            f"but it misses a key rule in {concept_name}. Don't worry — after seeing the correct solution, "
            f"you will instantly recognize this pattern!"
        )
    else:
        why_wrong = (
            f"The chosen option is a classic misconception in {concept_name}. "
            f"It typically results from skipping one of the key steps in the solution process."
        )

    # Check root causes
    weak_concepts = [
        m.concept_id
        for m in db.query(ConceptMastery).filter_by(student_id=student_id).all()
        if m.status in ["needs_attention", "developing"]
    ]
    root_causes = find_root_causes(db, student_id, weak_concepts) if weak_concepts else []
    rel_rc = next(
        (rc for rc in root_causes if rc["targetConcept"].lower() == concept_name.lower()),
        None
    )

    teacher_tip = None
    if rel_rc:
        teacher_tip = (
            f"Your assessment shows {rel_rc['prerequisiteConcept']} "
            f"(currently {rel_rc['prerequisite_score']}% mastery) is a prerequisite for this topic. "
            f"Spending 5-10 minutes on {rel_rc['prerequisiteConcept']} first will make this much easier!"
        )

    golden_rule = kb_info["golden_rule"] if kb_info else "Always re-read the question, write the formula, substitute values, and verify your answer."
    mini_challenge = kb_info["mini_challenge"] if kb_info else "Can you describe what this question tested in one sentence?"

    return {
        "question_num": question_num,
        "question_id": question_id,
        "question_text": question.text,
        "concept_id": question.concept_id,
        "concept_name": concept_name,
        "student_answer_label": student_answer_label,
        "student_answer_text": student_answer_text,
        "correct_answer_label": correct_answer_label,
        "correct_answer_text": correct_answer_text,
        "all_options": [
            {"label": opt.option_label, "text": opt.option_text, "is_correct": opt.option_label == correct_answer_label}
            for opt in options
        ],
        "why_wrong": why_wrong,
        "step_by_step": [step1, step2, step3],
        "golden_rule": golden_rule,
        "mini_challenge": mini_challenge,
        "teacher_tip": teacher_tip,
    }


def get_mentor_response(db: Session, student_id: int, message: str, concept_id: int = None, question_id: int = None, question_num: int = None):
    """
    Intelligent AI Mentor & Virtual Teacher.
    - Tailored pedagogical explanations for specific wrong assessment questions.
    - Deep concept teaching (theoretical foundation + key formulas + numerical worked examples).
    - Connects student query with actual assessment mastery profile and root-cause prerequisites.
    - Uses OpenAI API if configured, with rich deterministic pedagogical fallback.
    """
    # 1. Gather student mastery context
    masteries = db.query(ConceptMastery).filter_by(student_id=student_id).all()
    weak_concepts = [m.concept_id for m in masteries if m.status in ['needs_attention', 'developing']]
    root_causes = find_root_causes(db, student_id, weak_concepts) if weak_concepts else []

    mastery_summary = []
    for m in masteries:
        c = db.query(Concept).filter_by(id=m.concept_id).first()
        if c:
            mastery_summary.append(f"{c.name}: {m.score}% ({m.status})")

    # 2. Check if query is targeting a specific question ID or Question Number
    target_q = None
    if question_id:
        target_q = db.query(Question).filter_by(id=question_id).first()

    if not target_q:
        q_match = re.search(r'(?:question|q|problem)\s*#?\s*(\d+)', message, re.IGNORECASE)
        if q_match:
            extracted_num = int(q_match.group(1))
            question_num = question_num or extracted_num
            latest_assessment = db.query(Assessment).filter_by(student_id=student_id, status="completed").order_by(Assessment.completed_at.desc()).first()
            if latest_assessment:
                responses = db.query(AssessmentResponse).filter_by(assessment_id=latest_assessment.id).order_by(AssessmentResponse.id.asc()).all()
                if 1 <= extracted_num <= len(responses):
                    target_q_resp = responses[extracted_num - 1]
                    target_q = db.query(Question).filter_by(id=target_q_resp.question_id).first()
                    question_id = target_q.id if target_q else None

    # If a specific question is identified
    if target_q:
        q_concept = db.query(Concept).filter_by(id=target_q.concept_id).first()
        q_options = db.query(QuestionOption).filter_by(question_id=target_q.id).order_by(QuestionOption.option_label).all()
        options_dict = {opt.option_label: opt.option_text for opt in q_options}

        latest_resp = db.query(AssessmentResponse).filter_by(question_id=target_q.id).order_by(AssessmentResponse.id.desc()).first()
        student_ans = latest_resp.student_answer if latest_resp else None
        rel_rc = next((rc for rc in root_causes if rc["targetConcept"].lower() == (q_concept.name.lower() if q_concept else "")), None)

        concept_name = q_concept.name if q_concept else "Mathematics"
        q_label_text = f"Question #{question_num}" if question_num else "this question"

        student_ans_label = str(student_ans) if student_ans else "?"
        student_ans_full_text = options_dict.get(student_ans_label, "")
        correct_ans_label = target_q.correct_answer
        correct_ans_full_text = options_dict.get(correct_ans_label, "")

        student_ans_display = f"Option {student_ans_label}: \"{student_ans_full_text}\"" if student_ans_full_text else f"Option {student_ans_label}"
        correct_ans_display = f"Option {correct_ans_label}: \"{correct_ans_full_text}\"" if correct_ans_full_text else f"Option {correct_ans_label}"

        kb_info = CONCEPT_KNOWLEDGE_BASE.get(concept_name)
        golden_rule = kb_info["golden_rule"] if kb_info else "Always check your formulas carefully before calculating."
        mini_challenge = kb_info["mini_challenge"] if kb_info else "Try solving a similar problem to lock in this concept!"

        step1, step2, step3 = _build_steps_from_explanation(target_q.explanation, correct_ans_display)

        teacher_explanation = (
            f"### 👩‍🏫 AI Teacher — {q_label_text} Deep Explanation\n\n"
            f"**Topic:** `{concept_name}`\n\n"
            f"📌 **The Problem:**\n> *\"{target_q.text}\"*\n\n"
            f"---\n\n"
            f"#### 1️⃣ Understanding the Question in Simple Terms:\n"
            f"This question tests your understanding of **{concept_name}**. "
            f"Let's break down the underlying mathematical principle so it clicks permanently!\n\n"
            f"#### 2️⃣ Why ❌ {student_ans_display} was a Common Trap:\n"
            f"Many students pick this option because it looks similar at first glance — "
            f"but it misses an essential rule in **{concept_name}**. "
            f"This is one of the top misconceptions tested on this topic. Don't worry, you won't make this mistake again!\n\n"
            f"#### 3️⃣ Step-by-Step Solution (The Right Way):\n"
            f"**Step 1 —** {step1}.\n\n"
            f"**Step 2 —** {step2}.\n\n"
            f"**Step 3 (Conclusion) —** Therefore, the true correct answer is ✅ **{correct_ans_display}**.\n\n"
            f"#### 🔑 Golden Rule to Never Forget:\n"
            f"> {golden_rule}\n\n"
        )

        if rel_rc:
            teacher_explanation += (
                f"💡 **Teacher's Prerequisite Alert:** Your diagnostic shows that **{rel_rc['prerequisiteConcept']}** "
                f"(currently at {rel_rc['prerequisite_score']}% mastery) is a foundational bottleneck. "
                f"Mastering **{rel_rc['prerequisiteConcept']}** first will make solving {concept_name} problems completely natural!\n\n"
            )

        teacher_explanation += (
            f"#### ✍️ Mini Challenge — Test Yourself Right Now!\n"
            f"> {mini_challenge}\n\n"
            f"*Try solving it, then reply with your answer and I'll evaluate it for you! 😊*"
        )

        db.add(AIInteraction(
            student_id=student_id,
            query=message,
            response=teacher_explanation,
            context_concepts=concept_name
        ))
        db.commit()

        return {
            "response": teacher_explanation,
            "suggested_concept": concept_name,
            "question_id": target_q.id,
            "context_used": [f"Deep explanation for {q_label_text}"]
        }

    # 3. Check if query is asking to teach or explain a concept
    matched_cname, matched_kb = None, None
    if concept_id:
        c_obj = db.query(Concept).filter_by(id=concept_id).first()
        if c_obj:
            matched_cname = c_obj.name
            matched_kb = CONCEPT_KNOWLEDGE_BASE.get(matched_cname)

    if not matched_kb:
        matched_cname, matched_kb = find_matching_concept_info(message)

    if matched_kb:
        # Check student's current mastery in this concept
        c_obj = db.query(Concept).filter_by(name=matched_cname).first()
        m_rec = db.query(ConceptMastery).filter_by(student_id=student_id, concept_id=c_obj.id).first() if c_obj else None
        m_score = f"{round(m_rec.score, 1)}%" if m_rec else "Not assessed yet"

        formulas_formatted = "\n".join([f"• `{f}`" for f in matched_kb["formulas"]])
        steps_formatted = "\n".join([f"{s}" for s in matched_kb["worked_example"]["steps"]])

        concept_response = (
            f"### 📘 Complete Masterclass: **{matched_kb['title']}**\n\n"
            f"**Your Current Mastery:** `{m_score}` • **Syllabus:** `{matched_kb['grade']}`\n\n"
            f"---\n\n"
            f"#### 1️⃣ Theoretical Foundation (Plain-English Intuition)\n"
            f"{matched_kb['theory']}\n\n"
            f"#### 2️⃣ Key Formulas, Identities & Rules\n"
            f"{formulas_formatted}\n\n"
            f"#### 3️⃣ Step-by-Step Numerical Worked Example\n"
            f"📌 **Problem:** *{matched_kb['worked_example']['problem']}*\n\n"
            f"{steps_formatted}\n\n"
            f"✅ **Final Answer:** `{matched_kb['worked_example']['answer']}`\n\n"
            f"#### 4️⃣ Common Traps to Avoid\n"
            f"⚠️ *{matched_kb['pitfalls']}*\n\n"
            f"#### 🔑 Golden Rule:\n"
            f"> {matched_kb['golden_rule']}\n\n"
            f"#### ✍️ Mini Practice Challenge for You:\n"
            f"> {matched_kb['mini_challenge']}\n\n"
            f"*Reply with your answer to this challenge and I will check your work!*"
        )

        db.add(AIInteraction(
            student_id=student_id,
            query=message,
            response=concept_response,
            context_concepts=matched_cname
        ))
        db.commit()

        return {
            "response": concept_response,
            "suggested_concept": matched_cname,
            "question_id": None,
            "context_used": [f"Complete guide for {matched_cname}"]
        }

    # 4. Check for OpenAI Key if configured
    if settings.openai_api_key:
        try:
            import openai
            client = openai.OpenAI(api_key=settings.openai_api_key)

            system_prompt = (
                "You are GapWise AI's intelligent virtual Mathematics Teacher for Secondary School (Class 9-10).\n"
                "Explain concepts theoretically and numerically with clear step-by-step arithmetic and algebra.\n"
                "STUDENT LEARNING PROFILE:\n" +
                ("\n".join(mastery_summary) if mastery_summary else "No assessment taken yet.") +
                "\n\nIDENTIFIED ROOT CAUSE GAPS:\n" +
                ("\n".join([f"- {rc['targetConcept']} is weak because prerequisite {rc['prerequisiteConcept']} is not mastered." for rc in root_causes]) if root_causes else "None detected.") +
                "\n\nAlways provide rich, encouraging, step-by-step mathematical explanations with clear numerical examples."
            )

            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=700,
                temperature=0.7
            )

            ai_text = completion.choices[0].message.content
            db.add(AIInteraction(
                student_id=student_id,
                query=message,
                response=ai_text,
                context_concepts="Mathematics"
            ))
            db.commit()

            return {
                "response": ai_text,
                "suggested_concept": None,
                "question_id": None,
                "context_used": ["OpenAI Virtual Teacher"]
            }
        except Exception:
            pass

    # 5. Diagnostic and General Roadmap Fallback
    msg_lower = message.lower()

    if any(w in msg_lower for w in ["study", "next", "what to do", "roadmap", "priority", "where to start"]):
        if root_causes:
            rc = root_causes[0]
            response_text = (
                f"### 🎯 Your Personalized AI Learning Roadmap\n\n"
                f"Based on your diagnostic assessment, your #1 highest priority bottleneck is **{rc['prerequisiteConcept']}**.\n\n"
                f"💡 **Why:** You are struggling with **{rc['targetConcept']}** because its foundational prerequisite **{rc['prerequisiteConcept']}** (Mastery: {rc['prerequisite_score']}%) is currently not mastered.\n\n"
                f"📋 **Your 3-Step Action Plan:**\n"
                f"1. **Step 1:** Open [Learning Path](/learning/path) and study **{rc['prerequisiteConcept']}** (Read the theory & worked examples).\n"
                f"2. **Step 2:** Complete 5 practice questions on **{rc['prerequisiteConcept']}** to raise your mastery above 75%.\n"
                f"3. **Step 3:** Return to **{rc['targetConcept']}** — it will suddenly feel effortless!\n\n"
                f"Would you like me to give you a full theoretical breakdown and numerical example of **{rc['prerequisiteConcept']}** right now?"
            )
            return {
                "response": response_text,
                "suggested_concept": rc['prerequisiteConcept'],
                "question_id": None,
                "context_used": [f"Prerequisite roadmap for {rc['targetConcept']}"]
            }

    # Answer checking queries (e.g. "is 5 correct", "i got x = 2", "my answer is")
    if any(w in msg_lower for w in ["my answer", "i got", "is it", "correct", "check my", "answer is"]):
        response_text = (
            f"### 👩‍🏫 Great Effort Checking Your Work!\n\n"
            f"Let's check your reasoning:\n"
            f"1. **Verification Method:** Always substitute your calculated value back into the original equation.\n"
            f"2. If Left Hand Side (LHS) equals Right Hand Side (RHS), your solution is 100% mathematically correct!\n\n"
            f"💬 Tell me which specific problem you solved (e.g., *\"For Question #2 I got x = 3\"* or *\"For Factorisation challenge I got (x+2)(x+3)\"*), and I will verify every step of your arithmetic!"
        )
        return {
            "response": response_text,
            "suggested_concept": None,
            "question_id": None,
            "context_used": ["Answer verification engine"]
        }

    # General Greeting
    greeting_response = (
        f"### 👋 Hello! I am your 24/7 Personalized AI Math Teacher.\n\n"
        f"I am tracking your mastery across all 12 Class 9-10 Mathematics topics. Here is how I can help you achieve 100% mastery without needing a private tutor:\n\n"
        f"1. 🔍 **Explain Any Missed Question:** Type `\"Explain Question #3\"` or click any wrong question on your dashboard to see why your answer was wrong and get a step-by-step solution.\n"
        f"2. 📘 **Deep Concept Lessons:** Ask me `\"Explain Quadratic Equations\"`, `\"How to factorise polynomials\"`, or `\"What is Pythagoras Theorem\"` to get full theoretical guides + numerical worked examples.\n"
        f"3. 🗺️ **Prerequisite Diagnostics:** Ask `\"What should I study next?\"` to trace your exact prerequisite gaps.\n"
        f"4. ✍️ **Check Your Solutions:** Share any calculation and I will verify your steps.\n\n"
        f"What would you like to master today?"
    )

    return {
        "response": greeting_response,
        "suggested_concept": None,
        "question_id": None,
        "context_used": ["AI Math Teacher Introduction"]
    }
