SUBJECTS = [
    {
        "name": "Mathematics",
        "description": "Foundational and advanced mathematics for Secondary School (Class 9 & 10 CBSE/State Board syllabus)."
    }
]

CONCEPTS = [
    {
        "name": "Number Systems",
        "description": "Rational & irrational numbers, real number representations, decimal expansions, and laws of exponents.",
        "difficulty": 1,
        "grade": "9"
    },
    {
        "name": "Basic Algebra",
        "description": "Algebraic expressions, variables, coefficients, terms, and addition/subtraction/multiplication of polynomials.",
        "difficulty": 1,
        "grade": "9"
    },
    {
        "name": "Linear Equations",
        "description": "Linear equations in one and two variables, algebraic solutions, and graphical representations.",
        "difficulty": 2,
        "grade": "9"
    },
    {
        "name": "Algebraic Identities",
        "description": "Standard expansion identities: (a+b)², (a-b)², (a²-b²), (x+a)(x+b), (a+b+c)², and cubic identities.",
        "difficulty": 2,
        "grade": "9"
    },
    {
        "name": "Factorisation",
        "description": "Factoring polynomials using common factors, grouping, algebraic identities, and splitting the middle term.",
        "difficulty": 3,
        "grade": "9"
    },
    {
        "name": "Quadratic Equations",
        "description": "Standard form ax² + bx + c = 0, solution by factoring, quadratic formula, discriminant, and nature of roots.",
        "difficulty": 3,
        "grade": "10"
    },
    {
        "name": "Polynomials",
        "description": "Degree of polynomial, zeros of quadratic and cubic polynomials, relationship between zeros and coefficients.",
        "difficulty": 3,
        "grade": "10"
    },
    {
        "name": "Triangles",
        "description": "Congruence criteria (SAS, ASA, SSS, RHS), similarity theorems (AAA, SAS, SSS), and Basic Proportionality Theorem.",
        "difficulty": 2,
        "grade": "9"
    },
    {
        "name": "Coordinate Geometry",
        "description": "Cartesian plane, plotting points, distance formula, section formula, and area of triangles.",
        "difficulty": 3,
        "grade": "10"
    },
    {
        "name": "Trigonometry Basics",
        "description": "Trigonometric ratios (sin, cos, tan, cosec, sec, cot), values for standard angles (0°, 30°, 45°, 60°, 90°).",
        "difficulty": 3,
        "grade": "10"
    },
    {
        "name": "Trigonometry Applications",
        "description": "Trigonometric identities (sin²θ + cos²θ = 1), angle of elevation, angle of depression, heights and distances.",
        "difficulty": 4,
        "grade": "10"
    },
    {
        "name": "Mensuration",
        "description": "Surface areas and volumes of combinations of solids: cylinders, cones, spheres, hemispheres, and frustums.",
        "difficulty": 3,
        "grade": "10"
    }
]

PREREQUISITES = [
    ("Basic Algebra", "Number Systems"),
    ("Linear Equations", "Basic Algebra"),
    ("Algebraic Identities", "Basic Algebra"),
    ("Factorisation", "Algebraic Identities"),
    ("Quadratic Equations", "Factorisation"),
    ("Quadratic Equations", "Linear Equations"),
    ("Polynomials", "Quadratic Equations"),
    ("Coordinate Geometry", "Linear Equations"),
    ("Coordinate Geometry", "Triangles"),
    ("Trigonometry Basics", "Triangles"),
    ("Trigonometry Applications", "Trigonometry Basics"),
    ("Mensuration", "Triangles")
]

QUESTIONS = [
    # 1. Number Systems
    {
        "concept_name": "Number Systems",
        "question_type": "mcq",
        "difficulty": 1,
        "text": "Which of the following is an irrational number?",
        "correct_answer": "C",
        "explanation": "√7 cannot be expressed in the form p/q where p and q are integers with q ≠ 0, making it irrational. √4 = 2, 0.375 is a terminating rational, and 22/7 is a rational fraction.",
        "options": [
            {"label": "A", "text": "√4", "is_correct": False},
            {"label": "B", "text": "0.375", "is_correct": False},
            {"label": "C", "text": "√7", "is_correct": True},
            {"label": "D", "text": "22/7", "is_correct": False}
        ]
    },
    {
        "concept_name": "Number Systems",
        "question_type": "mcq",
        "difficulty": 2,
        "text": "Simplify the expression: (3 + √3)(3 - √3).",
        "correct_answer": "B",
        "explanation": "Using the algebraic identity (a + b)(a - b) = a² - b², we have 3² - (√3)² = 9 - 3 = 6.",
        "options": [
            {"label": "A", "text": "9", "is_correct": False},
            {"label": "B", "text": "6", "is_correct": True},
            {"label": "C", "text": "3", "is_correct": False},
            {"label": "D", "text": "12", "is_correct": False}
        ]
    },

    # 2. Basic Algebra
    {
        "concept_name": "Basic Algebra",
        "question_type": "mcq",
        "difficulty": 1,
        "text": "What is the degree of the polynomial 4x³ - 5x² + 7x⁴ + 9?",
        "correct_answer": "D",
        "explanation": "The degree of a polynomial is the highest power of the variable x, which is 4 in 7x⁴.",
        "options": [
            {"label": "A", "text": "2", "is_correct": False},
            {"label": "B", "text": "3", "is_correct": False},
            {"label": "C", "text": "1", "is_correct": False},
            {"label": "D", "text": "4", "is_correct": True}
        ]
    },
    {
        "concept_name": "Basic Algebra",
        "question_type": "mcq",
        "difficulty": 2,
        "text": "If P(x) = 2x² - 3x + 5, what is the value of P(-2)?",
        "correct_answer": "A",
        "explanation": "P(-2) = 2(-2)² - 3(-2) + 5 = 2(4) + 6 + 5 = 8 + 6 + 5 = 19.",
        "options": [
            {"label": "A", "text": "19", "is_correct": True},
            {"label": "B", "text": "7", "is_correct": False},
            {"label": "C", "text": "15", "is_correct": False},
            {"label": "D", "text": "-3", "is_correct": False}
        ]
    },

    # 3. Linear Equations
    {
        "concept_name": "Linear Equations",
        "question_type": "mcq",
        "difficulty": 2,
        "text": "Solve for x: 3x - 7 = 2(x + 4).",
        "correct_answer": "C",
        "explanation": "3x - 7 = 2x + 8 => 3x - 2x = 8 + 7 => x = 15.",
        "options": [
            {"label": "A", "text": "x = 1", "is_correct": False},
            {"label": "B", "text": "x = 8", "is_correct": False},
            {"label": "C", "text": "x = 15", "is_correct": True},
            {"label": "D", "text": "x = -1", "is_correct": False}
        ]
    },
    {
        "concept_name": "Linear Equations",
        "question_type": "mcq",
        "difficulty": 2,
        "text": "The pair of linear equations 2x + 3y = 9 and 4x + 6y = 18 has:",
        "correct_answer": "B",
        "explanation": "Here a1/a2 = 2/4 = 1/2, b1/b2 = 3/6 = 1/2, c1/c2 = 9/18 = 1/2. Since a1/a2 = b1/b2 = c1/c2, the lines are coincident and have infinitely many solutions.",
        "options": [
            {"label": "A", "text": "A unique solution", "is_correct": False},
            {"label": "B", "text": "Infinitely many solutions", "is_correct": True},
            {"label": "C", "text": "No solution", "is_correct": False},
            {"label": "D", "text": "Exactly two solutions", "is_correct": False}
        ]
    },

    # 4. Algebraic Identities
    {
        "concept_name": "Algebraic Identities",
        "question_type": "mcq",
        "difficulty": 2,
        "text": "Expand: (2x + 3y)².",
        "correct_answer": "B",
        "explanation": "Using identity (a + b)² = a² + 2ab + b²: (2x)² + 2(2x)(3y) + (3y)² = 4x² + 12xy + 9y².",
        "options": [
            {"label": "A", "text": "4x² + 6xy + 9y²", "is_correct": False},
            {"label": "B", "text": "4x² + 12xy + 9y²", "is_correct": True},
            {"label": "C", "text": "2x² + 12xy + 3y²", "is_correct": False},
            {"label": "D", "text": "4x² + 9y²", "is_correct": False}
        ]
    },
    {
        "concept_name": "Algebraic Identities",
        "question_type": "mcq",
        "difficulty": 2,
        "text": "If x + 1/x = 5, what is the value of x² + 1/x²?",
        "correct_answer": "A",
        "explanation": "Squaring both sides: (x + 1/x)² = 5² => x² + 2 + 1/x² = 25 => x² + 1/x² = 25 - 2 = 23.",
        "options": [
            {"label": "A", "text": "23", "is_correct": True},
            {"label": "B", "text": "25", "is_correct": False},
            {"label": "C", "text": "27", "is_correct": False},
            {"label": "D", "text": "21", "is_correct": False}
        ]
    },

    # 5. Factorisation
    {
        "concept_name": "Factorisation",
        "question_type": "mcq",
        "difficulty": 3,
        "text": "Factorise the quadratic expression: x² - 7x + 12.",
        "correct_answer": "C",
        "explanation": "We need two numbers that multiply to 12 and add to -7. These numbers are -3 and -4. Thus, x² - 7x + 12 = (x - 3)(x - 4).",
        "options": [
            {"label": "A", "text": "(x + 3)(x + 4)", "is_correct": False},
            {"label": "B", "text": "(x - 2)(x - 6)", "is_correct": False},
            {"label": "C", "text": "(x - 3)(x - 4)", "is_correct": True},
            {"label": "D", "text": "(x + 1)(x - 12)", "is_correct": False}
        ]
    },
    {
        "concept_name": "Factorisation",
        "question_type": "mcq",
        "difficulty": 3,
        "text": "What are the factors of 4a² - 9b²?",
        "correct_answer": "A",
        "explanation": "Applying difference of squares a² - b² = (a - b)(a + b), (2a)² - (3b)² = (2a - 3b)(2a + 3b).",
        "options": [
            {"label": "A", "text": "(2a - 3b)(2a + 3b)", "is_correct": True},
            {"label": "B", "text": "(2a - 3b)²", "is_correct": False},
            {"label": "C", "text": "(4a - 9b)(a + b)", "is_correct": False},
            {"label": "D", "text": "(2a + 3b)²", "is_correct": False}
        ]
    },
    {
        "concept_name": "Factorisation",
        "question_type": "mcq",
        "difficulty": 3,
        "text": "Factorise 6x² + 11x + 3 by splitting the middle term.",
        "correct_answer": "D",
        "explanation": "Product = 6 * 3 = 18, Sum = 11. Numbers are 9 and 2. 6x² + 9x + 2x + 3 = 3x(2x + 3) + 1(2x + 3) = (2x + 3)(3x + 1).",
        "options": [
            {"label": "A", "text": "(6x + 1)(x + 3)", "is_correct": False},
            {"label": "B", "text": "(3x + 2)(2x + 1)", "is_correct": False},
            {"label": "C", "text": "(2x - 3)(3x - 1)", "is_correct": False},
            {"label": "D", "text": "(2x + 3)(3x + 1)", "is_correct": True}
        ]
    },

    # 6. Quadratic Equations
    {
        "concept_name": "Quadratic Equations",
        "question_type": "mcq",
        "difficulty": 3,
        "text": "Find the roots of the quadratic equation: x² - 5x + 6 = 0.",
        "correct_answer": "B",
        "explanation": "Factoring gives (x - 2)(x - 3) = 0. Therefore, the roots are x = 2 and x = 3.",
        "options": [
            {"label": "A", "text": "x = -2, -3", "is_correct": False},
            {"label": "B", "text": "x = 2, 3", "is_correct": True},
            {"label": "C", "text": "x = 1, 6", "is_correct": False},
            {"label": "D", "text": "x = -1, -6", "is_correct": False}
        ]
    },
    {
        "concept_name": "Quadratic Equations",
        "question_type": "mcq",
        "difficulty": 3,
        "text": "What is the discriminant of 2x² - 4x + 3 = 0, and what is the nature of its roots?",
        "correct_answer": "C",
        "explanation": "Discriminant D = b² - 4ac = (-4)² - 4(2)(3) = 16 - 24 = -8. Since D < 0, there are no real roots (complex roots).",
        "options": [
            {"label": "A", "text": "D = 8, real and distinct roots", "is_correct": False},
            {"label": "B", "text": "D = 0, two equal real roots", "is_correct": False},
            {"label": "C", "text": "D = -8, no real roots", "is_correct": True},
            {"label": "D", "text": "D = 40, real roots", "is_correct": False}
        ]
    },

    # 7. Polynomials
    {
        "concept_name": "Polynomials",
        "question_type": "mcq",
        "difficulty": 3,
        "text": "If α and β are the zeros of p(x) = x² - 7x + 10, find the value of α + β and αβ.",
        "correct_answer": "A",
        "explanation": "For ax² + bx + c: Sum of zeros α + β = -b/a = -(-7)/1 = 7. Product of zeros αβ = c/a = 10/1 = 10.",
        "options": [
            {"label": "A", "text": "α + β = 7, αβ = 10", "is_correct": True},
            {"label": "B", "text": "α + β = -7, αβ = 10", "is_correct": False},
            {"label": "C", "text": "α + β = 10, αβ = 7", "is_correct": False},
            {"label": "D", "text": "α + β = 7, αβ = -10", "is_correct": False}
        ]
    },
    {
        "concept_name": "Polynomials",
        "question_type": "mcq",
        "difficulty": 3,
        "text": "Find the remainder when f(x) = x³ - 3x² + 4x - 5 is divided by (x - 2).",
        "correct_answer": "D",
        "explanation": "By the Remainder Theorem, Remainder = f(2) = (2)³ - 3(2)² + 4(2) - 5 = 8 - 12 + 8 - 5 = -1.",
        "options": [
            {"label": "A", "text": "3", "is_correct": False},
            {"label": "B", "text": "1", "is_correct": False},
            {"label": "C", "text": "0", "is_correct": False},
            {"label": "D", "text": "-1", "is_correct": True}
        ]
    },

    # 8. Triangles
    {
        "concept_name": "Triangles",
        "question_type": "mcq",
        "difficulty": 2,
        "text": "In △ABC, DE || BC intersecting AB at D and AC at E. If AD = 2 cm, DB = 3 cm, and AE = 4 cm, find EC.",
        "correct_answer": "B",
        "explanation": "By Basic Proportionality Theorem (Thales's Theorem): AD/DB = AE/EC => 2/3 = 4/EC => EC = (3 * 4) / 2 = 6 cm.",
        "options": [
            {"label": "A", "text": "5 cm", "is_correct": False},
            {"label": "B", "text": "6 cm", "is_correct": True},
            {"label": "C", "text": "8 cm", "is_correct": False},
            {"label": "D", "text": "4.5 cm", "is_correct": False}
        ]
    },
    {
        "concept_name": "Triangles",
        "question_type": "mcq",
        "difficulty": 2,
        "text": "The lengths of sides of four triangles are given below. Which one forms a right-angled triangle?",
        "correct_answer": "C",
        "explanation": "Check Pythagoras theorem a² + b² = c²: For 6 cm, 8 cm, 10 cm: 6² + 8² = 36 + 64 = 100 = 10². Hence, it is a right triangle.",
        "options": [
            {"label": "A", "text": "3 cm, 4 cm, 6 cm", "is_correct": False},
            {"label": "B", "text": "5 cm, 8 cm, 11 cm", "is_correct": False},
            {"label": "C", "text": "6 cm, 8 cm, 10 cm", "is_correct": True},
            {"label": "D", "text": "7 cm, 9 cm, 12 cm", "is_correct": False}
        ]
    },

    # 9. Coordinate Geometry
    {
        "concept_name": "Coordinate Geometry",
        "question_type": "mcq",
        "difficulty": 3,
        "text": "Find the distance between the points A(2, 3) and B(6, 6).",
        "correct_answer": "A",
        "explanation": "Distance formula d = √[(x2 - x1)² + (y2 - y1)²] = √[(6 - 2)² + (6 - 3)²] = √[4² + 3²] = √[16 + 9] = √25 = 5 units.",
        "options": [
            {"label": "A", "text": "5 units", "is_correct": True},
            {"label": "B", "text": "7 units", "is_correct": False},
            {"label": "C", "text": "√13 units", "is_correct": False},
            {"label": "D", "text": "25 units", "is_correct": False}
        ]
    },
    {
        "concept_name": "Coordinate Geometry",
        "question_type": "mcq",
        "difficulty": 3,
        "text": "The coordinates of the midpoint of the line segment joining (4, -2) and (8, 6) are:",
        "correct_answer": "D",
        "explanation": "Midpoint M = ((x1 + x2)/2, (y1 + y2)/2) = ((4 + 8)/2, (-2 + 6)/2) = (12/2, 4/2) = (6, 2).",
        "options": [
            {"label": "A", "text": "(4, 2)", "is_correct": False},
            {"label": "B", "text": "(12, 4)", "is_correct": False},
            {"label": "C", "text": "(2, 4)", "is_correct": False},
            {"label": "D", "text": "(6, 2)", "is_correct": True}
        ]
    },

    # 10. Trigonometry Basics
    {
        "concept_name": "Trigonometry Basics",
        "question_type": "mcq",
        "difficulty": 3,
        "text": "If tan θ = 4/3, what is the value of sin θ?",
        "correct_answer": "C",
        "explanation": "In a right triangle, tan θ = Opposite/Adjacent = 4/3. Hypotenuse = √(4² + 3²) = 5. Therefore, sin θ = Opposite/Hypotenuse = 4/5.",
        "options": [
            {"label": "A", "text": "3/5", "is_correct": False},
            {"label": "B", "text": "3/4", "is_correct": False},
            {"label": "C", "text": "4/5", "is_correct": True},
            {"label": "D", "text": "5/4", "is_correct": False}
        ]
    },
    {
        "concept_name": "Trigonometry Basics",
        "question_type": "mcq",
        "difficulty": 3,
        "text": "Evaluate: sin 30° + cos 60° - tan 45°.",
        "correct_answer": "B",
        "explanation": "sin 30° = 1/2, cos 60° = 1/2, tan 45° = 1. Value = 1/2 + 1/2 - 1 = 1 - 1 = 0.",
        "options": [
            {"label": "A", "text": "1", "is_correct": False},
            {"label": "B", "text": "0", "is_correct": True},
            {"label": "C", "text": "1/2", "is_correct": False},
            {"label": "D", "text": "√3/2", "is_correct": False}
        ]
    },

    # 11. Trigonometry Applications
    {
        "concept_name": "Trigonometry Applications",
        "question_type": "mcq",
        "difficulty": 4,
        "text": "A vertical pole of height 10 m casts a shadow of 10√3 m on the ground. Find the sun's angle of elevation.",
        "correct_answer": "A",
        "explanation": "tan θ = Height / Shadow = 10 / (10√3) = 1/√3. Since tan 30° = 1/√3, the angle of elevation is 30°.",
        "options": [
            {"label": "A", "text": "30°", "is_correct": True},
            {"label": "B", "text": "45°", "is_correct": False},
            {"label": "C", "text": "60°", "is_correct": False},
            {"label": "D", "text": "90°", "is_correct": False}
        ]
    },
    {
        "concept_name": "Trigonometry Applications",
        "question_type": "mcq",
        "difficulty": 4,
        "text": "Simplify: (sin θ / (1 + cos θ)) + ((1 + cos θ) / sin θ).",
        "correct_answer": "C",
        "explanation": "[sin²θ + (1 + cos θ)²] / [sin θ(1 + cos θ)] = [sin²θ + 1 + 2cos θ + cos²θ] / [sin θ(1 + cos θ)] = [2 + 2cos θ] / [sin θ(1 + cos θ)] = 2(1 + cos θ) / [sin θ(1 + cos θ)] = 2 / sin θ = 2 cosec θ.",
        "options": [
            {"label": "A", "text": "2 sec θ", "is_correct": False},
            {"label": "B", "text": "2 tan θ", "is_correct": False},
            {"label": "C", "text": "2 cosec θ", "is_correct": True},
            {"label": "D", "text": "cosec θ", "is_correct": False}
        ]
    },

    # 12. Mensuration
    {
        "concept_name": "Mensuration",
        "question_type": "mcq",
        "difficulty": 3,
        "text": "Find the total surface area of a solid hemisphere of radius 7 cm (Take π = 22/7).",
        "correct_answer": "B",
        "explanation": "Total surface area of a solid hemisphere = 3πr² = 3 * (22/7) * 7 * 7 = 3 * 22 * 7 = 462 cm².",
        "options": [
            {"label": "A", "text": "308 cm²", "is_correct": False},
            {"label": "B", "text": "462 cm²", "is_correct": True},
            {"label": "C", "text": "616 cm²", "is_correct": False},
            {"label": "D", "text": "154 cm²", "is_correct": False}
        ]
    },
    {
        "concept_name": "Mensuration",
        "question_type": "mcq",
        "difficulty": 3,
        "text": "A cylinder and a cone have equal bases and equal heights. What is the ratio of their volumes?",
        "correct_answer": "D",
        "explanation": "Volume of cylinder = πr²h, Volume of cone = (1/3)πr²h. Ratio = πr²h : (1/3)πr²h = 3 : 1.",
        "options": [
            {"label": "A", "text": "1 : 3", "is_correct": False},
            {"label": "B", "text": "1 : 1", "is_correct": False},
            {"label": "C", "text": "2 : 1", "is_correct": False},
            {"label": "D", "text": "3 : 1", "is_correct": True}
        ]
    }
]

# Comprehensive educational content for all 12 concepts
LEARNING_RESOURCES = {
    "Number Systems": {
        "explanation": "Number systems are the foundation of all mathematics. Real numbers are divided into rational numbers (expressible as p/q where q ≠ 0) and irrational numbers (non-terminating, non-repeating decimals such as √2, π). Every real number corresponds to a unique point on the number line. Understanding rationalization of denominators and laws of integral and rational exponents allows us to simplify complex radical terms.",
        "key_ideas": [
            "Rational numbers have terminating or recurring decimal expansions.",
            "Irrational numbers have non-terminating and non-recurring expansions.",
            "To rationalize 1/(a + √b), multiply numerator and denominator by conjugate (a - √b).",
            "Laws of exponents: aᵐ × aⁿ = aᵐ⁺ⁿ, (aᵐ)ⁿ = aᵐⁿ, and a⁻ⁿ = 1/aⁿ."
        ],
        "worked_example": "Problem: Rationalize the denominator of 1 / (3 + √2).\nStep 1: Identify conjugate of denominator: (3 - √2).\nStep 2: Multiply top and bottom: (3 - √2) / [(3 + √2)(3 - √2)].\nStep 3: Apply (a + b)(a - b) = a² - b²: (3 - √2) / (3² - (√2)²) = (3 - √2) / (9 - 2) = (3 - √2)/7.",
        "common_mistakes": [
            "Assuming √4 or √9 are irrational because of the square root symbol.",
            "Forgetting to apply exponent laws to both numerator and denominator in fractional powers.",
            "Adding square roots incorrectly: √(a + b) ≠ √a + √b."
        ]
    },
    "Basic Algebra": {
        "explanation": "Basic algebra introduces symbolic reasoning through variables and algebraic expressions. An expression combines constants, variables, and mathematical operators. Polynomials are algebraic expressions where variable powers are non-negative integers. Mastering polynomial arithmetic (addition, subtraction, and distributive multiplication) is the essential gateway to solving equations.",
        "key_ideas": [
            "Like terms have the same variables raised to the identical powers (e.g., 3x²y and -5x²y).",
            "Degree of a polynomial is the highest power of the variable in any non-zero term.",
            "Distributive property: a(b + c) = ab + ac.",
            "Polynomials cannot have negative or fractional powers of the variable."
        ],
        "worked_example": "Problem: Multiply (2x - 3) by (3x² + 4x - 1).\nStep 1: Distribute 2x: 2x(3x² + 4x - 1) = 6x³ + 8x² - 2x.\nStep 2: Distribute -3: -3(3x² + 4x - 1) = -9x² - 12x + 3.\nStep 3: Combine like terms: 6x³ + (8x² - 9x²) + (-2x - 12x) + 3 = 6x³ - x² - 14x + 3.",
        "common_mistakes": [
            "Combining unlike terms (e.g., writing 3x + 2x² = 5x³).",
            "Dropping negative signs when distributing subtraction across parentheses.",
            "Confusing 2x with x²."
        ]
    },
    "Linear Equations": {
        "explanation": "A linear equation is a statement of equality where variables appear with an exponent of 1. Linear equations in one variable can be solved through inverse operations. Linear equations in two variables (ax + by + c = 0) represent straight lines on the Cartesian plane. A system of two linear equations can be solved algebraically using substitution, elimination, or cross-multiplication.",
        "key_ideas": [
            "Standard form of linear equation in two variables: ax + by + c = 0.",
            "A pair of lines has a unique solution if a1/a2 ≠ b1/b2 (intersecting lines).",
            "Infinitely many solutions occur if a1/a2 = b1/b2 = c1/c2 (coincident lines).",
            "No solution occurs if a1/a2 = b1/b2 ≠ c1/c2 (parallel lines)."
        ],
        "worked_example": "Problem: Solve by elimination: 2x + 3y = 8 and 3x + 2y = 7.\nStep 1: Multiply eq 1 by 3: 6x + 9y = 24.\nStep 2: Multiply eq 2 by 2: 6x + 4y = 14.\nStep 3: Subtract: 5y = 10 => y = 2.\nStep 4: Substitute y=2 into eq 1: 2x + 6 = 8 => 2x = 2 => x = 1. Solution: (1, 2).",
        "common_mistakes": [
            "Forgetting to multiply both sides of the equation by the multiplier.",
            "Sign errors during subtraction of simultaneous equations.",
            "Confusing parallel lines (no solution) with intersecting lines."
        ]
    },
    "Algebraic Identities": {
        "explanation": "Algebraic identities are equality statements that hold true for all values of their variables. They serve as mathematical shortcuts for expanding products and factoring expressions. Key identities include square of binomials (a ± b)², difference of squares (a² - b²), square of trinomials (a + b + c)², and cubes of binomials (a ± b)³.",
        "key_ideas": [
            "(a + b)² = a² + 2ab + b² and (a - b)² = a² - 2ab + b².",
            "Difference of squares: a² - b² = (a - b)(a + b).",
            "Trinomial square: (a + b + c)² = a² + b² + c² + 2ab + 2bc + 2ca.",
            "Cubes: (a + b)³ = a³ + b³ + 3ab(a + b) and a³ + b³ = (a + b)(a² - ab + b²)."
        ],
        "worked_example": "Problem: Evaluate 103 × 97 using algebraic identities.\nStep 1: Rewrite as (100 + 3)(100 - 3).\nStep 2: Apply (a + b)(a - b) = a² - b².\nStep 3: Calculate 100² - 3² = 10,000 - 9 = 9,991.",
        "common_mistakes": [
            "Writing (a + b)² = a² + b² (missing the middle 2ab term!).",
            "Misidentifying signs in (a - b)³: the expansion is a³ - 3a²b + 3ab² - b³.",
            "Confusing (a³ - b³) with (a - b)³."
        ]
    },
    "Factorisation": {
        "explanation": "Factorisation is the process of writing an algebraic expression as the product of its irreducible factors. It is the inverse of polynomial expansion and is the fundamental technique required for solving quadratic equations and simplifying rational expressions. Core methods include taking out common factors, grouping terms, applying identities (a² - b²), and splitting the middle term for quadratic trinomials ax² + bx + c.",
        "key_ideas": [
            "Always inspect for a greatest common factor (GCF) first.",
            "Difference of two squares pattern: x² - y² = (x - y)(x + y).",
            "Splitting middle term for ax² + bx + c: Find two numbers p and q such that p × q = a × c and p + q = b.",
            "Grouping technique: Pair terms with common factors, e.g., ax + ay + bx + by = a(x + y) + b(x + y) = (x + y)(a + b)."
        ],
        "worked_example": "Problem: Factorise 2x² + 7x + 3.\nStep 1: Product ac = 2 × 3 = 6. Sum b = 7.\nStep 2: Two numbers multiplying to 6 and adding to 7 are 6 and 1.\nStep 3: Split middle term: 2x² + 6x + x + 3.\nStep 4: Group: 2x(x + 3) + 1(x + 3) = (2x + 1)(x + 3).",
        "common_mistakes": [
            "Choosing two numbers that satisfy the sum but not the product ac.",
            "Forgetting the sign of ac (e.g. in x² - 5x - 6, numbers are -6 and +1, not -2 and -3).",
            "Failing to factor out a constant factor first before splitting the middle term."
        ]
    },
    "Quadratic Equations": {
        "explanation": "A quadratic equation is a second-degree polynomial equation of the form ax² + bx + c = 0 (where a ≠ 0). Solving quadratics can be done by factorisation, completing the square, or using the Quadratic Formula: x = [-b ± √(b² - 4ac)] / (2a). The discriminant D = b² - 4ac determines the nature of the roots without explicitly solving the equation.",
        "key_ideas": [
            "Standard form must always be set to zero: ax² + bx + c = 0.",
            "If D = b² - 4ac > 0: Two distinct real roots.",
            "If D = 0: Two equal real roots (x = -b / 2a).",
            "If D < 0: No real roots (roots are complex).",
            "Strong factorisation skills are a strict prerequisite for solving quadratics by factoring."
        ],
        "worked_example": "Problem: Solve 3x² - 5x + 2 = 0 using the quadratic formula.\nStep 1: Identify a = 3, b = -5, c = 2.\nStep 2: Compute Discriminant D = (-5)² - 4(3)(2) = 25 - 24 = 1.\nStep 3: Apply formula: x = [-(-5) ± √1] / (2 × 3) = (5 ± 1) / 6.\nStep 4: x1 = (5 + 1)/6 = 1, x2 = (5 - 1)/6 = 4/6 = 2/3. Roots are 1 and 2/3.",
        "common_mistakes": [
            "Applying the formula before converting the equation into standard ax² + bx + c = 0 form.",
            "Sign errors with -b: if b = -5, then -b is +5.",
            "Forgetting to divide the entire numerator by 2a, not just the radical."
        ]
    },
    "Polynomials": {
        "explanation": "Polynomial theory explores the mathematical properties of functions of the form P(x) = aₙxⁿ + ... + a₀. The zeros of a polynomial are values of k for which P(k) = 0. For quadratic polynomial ax² + bx + c, the sum of zeros is -b/a and product of zeros is c/a. The Remainder and Factor Theorems connect zeros directly to linear polynomial divisors.",
        "key_ideas": [
            "For quadratic polynomial ax² + bx + c with zeros α, β: α + β = -b/a and αβ = c/a.",
            "Factor Theorem: (x - a) is a factor of P(x) if and only if P(a) = 0.",
            "Remainder Theorem: When P(x) is divided by (x - a), the remainder is P(a).",
            "A polynomial of degree n has at most n real zeros."
        ],
        "worked_example": "Problem: Find a quadratic polynomial whose sum and product of zeros are -3 and 2.\nStep 1: General form is k[x² - (Sum)x + Product].\nStep 2: Substitute values: k[x² - (-3)x + 2] = k[x² + 3x + 2].\nStep 3: Setting k=1 gives the polynomial: x² + 3x + 2.",
        "common_mistakes": [
            "Swapping sum and product coefficients (forgetting the negative sign in x² - Sx + P).",
            "Confusing zeros of a polynomial with factors: if zero is 3, factor is (x - 3)."
        ]
    },
    "Triangles": {
        "explanation": "Triangles are geometric shapes formed by three line segments. Two triangles are congruent if all corresponding sides and angles are equal. They are similar if corresponding angles are equal and corresponding sides are in the same ratio. The Basic Proportionality Theorem (Thales's Theorem) and Pythagoras theorem are cornerstones of geometric proof and measurement.",
        "key_ideas": [
            "Criteria for similarity: AAA (or AA), SAS, SSS.",
            "Basic Proportionality Theorem: A line drawn parallel to one side of a triangle divides the other two sides in the same ratio.",
            "Ratio of areas of two similar triangles equals the ratio of squares of their corresponding sides.",
            "Pythagoras Theorem: In a right triangle, hypotenuse² = base² + perpendicular²."
        ],
        "worked_example": "Problem: In △ABC, DE || BC with AD = 3 cm, BD = 4 cm, AE = 6 cm. Find AC.\nStep 1: By Thales theorem, AD/BD = AE/CE.\nStep 2: 3/4 = 6/CE => 3 × CE = 24 => CE = 8 cm.\nStep 3: AC = AE + CE = 6 + 8 = 14 cm.",
        "common_mistakes": [
            "Using Thales theorem ratios incorrectly (confusing AD/AB with AD/DB).",
            "Assuming triangles are congruent when they are only similar."
        ]
    },
    "Coordinate Geometry": {
        "explanation": "Coordinate geometry links algebraic equations with geometric figures on the 2D Cartesian plane. Any point is represented by ordered pair (x, y). We can calculate the distance between two points, find the coordinates of a point dividing a segment in a given ratio (Section Formula), and calculate areas of polygons.",
        "key_ideas": [
            "Distance Formula: d = √[(x₂ - x₁)² + (y₂ - y₁)²].",
            "Midpoint Formula: M = ((x₁ + x₂)/2, (y₁ + y₂)/2).",
            "Section Formula: P = ((m₁x₂ + m₂x₁)/(m₁ + m₂), (m₁y₂ + m₂y₁)/(m₁ + m₂)).",
            "Collinear points: Three points are collinear if the area of the triangle formed by them is 0."
        ],
        "worked_example": "Problem: Find point P dividing segment joining A(1, 3) and B(4, 6) in ratio 2:1.\nStep 1: m1 = 2, m2 = 1, (x1, y1) = (1, 3), (x2, y2) = (4, 6).\nStep 2: x = (2×4 + 1×1)/(2+1) = (8 + 1)/3 = 9/3 = 3.\nStep 3: y = (2×6 + 1×3)/(2+1) = (12 + 3)/3 = 15/3 = 5. Coordinates of P are (3, 5).",
        "common_mistakes": [
            "Reversing coordinates x and y in formulas.",
            "Incorrectly applying ratio m1:m2 to (x1, y1) instead of (x2, y2)."
        ]
    },
    "Trigonometry Basics": {
        "explanation": "Trigonometry studies the relationships between side lengths and angles in right-angled triangles. The six primary trigonometric ratios are defined relative to an acute angle θ: sin θ (Opp/Hyp), cos θ (Adj/Hyp), tan θ (Opp/Adj), and their reciprocals cosec θ, sec θ, cot θ. Knowing standard angle values (0°, 30°, 45°, 60°, 90°) is critical for problem solving.",
        "key_ideas": [
            "sin θ = Opp/Hyp, cos θ = Adj/Hyp, tan θ = Opp/Adj.",
            "Reciprocal relations: cosec θ = 1/sin θ, sec θ = 1/cos θ, cot θ = 1/tan θ.",
            "tan θ = sin θ / cos θ and cot θ = cos θ / sin θ.",
            "Values: sin 30° = 1/2, cos 30° = √3/2, tan 45° = 1, sin 90° = 1."
        ],
        "worked_example": "Problem: If sin A = 3/5, find cos A and tan A for acute angle A.\nStep 1: Opp = 3, Hyp = 5. By Pythagoras, Adj = √(5² - 3²) = √(25 - 9) = 4.\nStep 2: cos A = Adj/Hyp = 4/5.\nStep 3: tan A = Opp/Adj = 3/4.",
        "common_mistakes": [
            "Mixing up Opposite and Adjacent sides when the reference angle shifts from A to C.",
            "Thinking sin θ means sin multiplied by θ (it is a trigonometric function, not a product!)."
        ]
    },
    "Trigonometry Applications": {
        "explanation": "Applications of trigonometry utilize trigonometric ratios to calculate real-world measurements such as heights of structures, distances between objects, and angles of elevation/depression. The angle of elevation is the angle formed above the horizontal line of sight to an elevated object, while the angle of depression is formed looking downwards.",
        "key_ideas": [
            "Pythagorean Identities: sin²θ + cos²θ = 1, 1 + tan²θ = sec²θ, 1 + cot²θ = cosec²θ.",
            "Angle of elevation: Observer looks UP at object (Angle measured from horizontal).",
            "Angle of depression: Observer looks DOWN at object (equals angle of elevation from object to observer by alternate interior angles).",
            "Use tan θ = Height/Distance in most single-triangle elevation problems."
        ],
        "worked_example": "Problem: A ladder leaning against a wall makes an angle of 60° with the ground. If the foot of the ladder is 2.5 m from the wall, find ladder length.\nStep 1: cos 60° = Base / Hypotenuse.\nStep 2: 1/2 = 2.5 / Length.\nStep 3: Length = 2.5 × 2 = 5 meters.",
        "common_mistakes": [
            "Measuring angle of depression from vertical wall instead of horizontal line of sight.",
            "Using sin instead of tan when height and shadow length are provided."
        ]
    },
    "Mensuration": {
        "explanation": "Mensuration deals with calculating perimeters, surface areas, and volumes of 2D and 3D geometric shapes. For Class 10, problems focus on combinations and conversions of standard solids: cuboids, cylinders, cones, spheres, and hemispheres. When one solid is melted and recast into another, the total volume remains constant.",
        "key_ideas": [
            "Cylinder: Curved Surface Area = 2πrh, Volume = πr²h.",
            "Cone: Slant height l = √(r² + h²), Curved Surface Area = πrl, Volume = (1/3)πr²h.",
            "Sphere: Surface Area = 4πr², Volume = (4/3)πr³.",
            "Solid Hemisphere: Total Surface Area = 3πr², Volume = (2/3)πr³.",
            "Volume conservation: Volume before conversion = Volume after conversion."
        ],
        "worked_example": "Problem: A metallic sphere of radius 4.2 cm is melted and recast into a cylinder of radius 6 cm. Find cylinder height.\nStep 1: Vol of sphere = Vol of cylinder => (4/3)πr₁³ = πr₂²h.\nStep 2: (4/3) × (4.2)³ = 6² × h => (4/3) × 74.088 = 36h.\nStep 3: 98.784 = 36h => h = 98.784 / 36 = 2.74 cm.",
        "common_mistakes": [
            "Using radius instead of diameter or vice-versa in formulas.",
            "Confusing vertical height h with slant height l in cone surface area calculations.",
            "Using 2πr² for total surface area of a solid hemisphere instead of 3πr²."
        ]
    }
}
