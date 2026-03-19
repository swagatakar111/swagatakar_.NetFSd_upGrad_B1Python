
const courses = [
  {
    id: 1,
    name: "JavaScript",
    lessons: [
      { day: 1, title: "Introduction to JavaScript", topics: ["What is JS?", "History & Uses", "Setting up environment"] },
      { day: 2, title: "Variables & Data Types", topics: ["var, let, const", "Strings, Numbers, Booleans", "typeof operator"] },
      { day: 3, title: "Functions & Scope", topics: ["Function declaration", "Arrow functions", "Scope & closures"] },
      { day: 4, title: "Arrays & Objects", topics: ["Array methods", "Object literals", "Destructuring"] },
      { day: 5, title: "DOM & Events", topics: ["Selecting elements", "Event listeners", "Manipulating the DOM"] }
    ]
  },
  {
    id: 2,
    name: "HTML & CSS",
    lessons: [
      { day: 1, title: "HTML Basics", topics: ["HTML structure", "Tags & attributes", "Headings, paragraphs, links"] },
      { day: 2, title: "HTML Forms & Tables", topics: ["Form elements", "Input types", "Table structure"] },
      { day: 3, title: "CSS Fundamentals", topics: ["Selectors", "Colors & fonts", "Box model"] },
      { day: 4, title: "Layouts", topics: ["Flexbox", "CSS Grid", "Positioning"] },
      { day: 5, title: "Responsive Design", topics: ["Media queries", "Mobile-first approach", "Viewport units"] }
    ]
  },
  {
    id: 3,
    name: "React Basics",
    lessons: [
      { day: 1, title: "Intro to React", topics: ["What is React?", "Virtual DOM", "Create React App"] },
      { day: 2, title: "Components & JSX", topics: ["Functional components", "JSX syntax", "Rendering elements"] },
      { day: 3, title: "Props & State", topics: ["Passing props", "useState hook", "Re-rendering"] },
      { day: 4, title: "Events & Lists", topics: ["Handling events", "Rendering lists", "Keys in React"] },
      { day: 5, title: "Hooks & API", topics: ["useEffect hook", "Fetching data", "Lifecycle basics"] }
    ]
  },
  {
    id: 4,
    name: "Node.js",
    lessons: [
      { day: 1, title: "Intro to Node.js", topics: ["What is Node?", "V8 engine", "Installing Node & NPM"] },
      { day: 2, title: "Core Modules", topics: ["fs module", "http module", "path module"] },
      { day: 3, title: "Express Framework", topics: ["Setting up Express", "Routes", "Middleware"] },
      { day: 4, title: "Async JavaScript", topics: ["Callbacks", "Promises", "async/await"] },
      { day: 5, title: "REST APIs", topics: ["GET & POST requests", "JSON responses", "Connecting to frontend"] }
    ]
  }
];

const quizData = {


  1: {
    quiz1: [
      { question: "JS is?", options: ["Language", "Tool", "DB"], answer: 0 },
      { question: "var is?", options: ["keyword", "loop", "tag"], answer: 0 },
      { question: "typeof null?", options: ["object", "null", "undefined"], answer: 0 },
      { question: "Array syntax?", options: ["[]", "{}", "()"], answer: 0 },
      { question: "Loop?", options: ["for", "if", "var"], answer: 0 }
    ],
    quiz2: [
      { question: "NaN means?", options: ["Not a Number", "Name", "Null"], answer: 0 },
      { question: "JS runs on?", options: ["Browser", "CPU", "RAM"], answer: 0 },
      { question: "Object syntax?", options: ["{}", "[]", "()"], answer: 0 },
      { question: "Comment symbol?", options: ["//", "**", "##"], answer: 0 },
      { question: "JS is?", options: ["Dynamic", "Static", "None"], answer: 0 }
    ]
  },

  2: {
    quiz1: [
      { question: "HTML stands for?", options: ["Markup", "Style", "Logic"], answer: 0 },
      { question: "CSS is used for?", options: ["Styling", "Logic", "DB"], answer: 0 },
      { question: "Image tag?", options: ["img", "pic", "image"], answer: 0 },
      { question: "Link tag?", options: ["a", "href", "link"], answer: 0 },
      { question: "h1 is?", options: ["Heading", "Paragraph", "Div"], answer: 0 }
    ],
    quiz2: [
      { question: "ul tag?", options: ["List", "Table", "Form"], answer: 0 },
      { question: "p tag?", options: ["Paragraph", "Image", "List"], answer: 0 },
      { question: "CSS Grid?", options: ["Layout", "Tag", "Function"], answer: 0 },
      { question: "Flexbox?", options: ["Layout", "DB", "Language"], answer: 0 },
      { question: "color is?", options: ["CSS property", "HTML tag", "JS function"], answer: 0 }
    ]
  },

  3: {
    quiz1: [
      { question: "React is?", options: ["Library", "Language", "DB"], answer: 0 },
      { question: "Component is?", options: ["Reusable UI", "DB", "Loop"], answer: 0 },
      { question: "JSX stands for?", options: ["JS XML", "Java Syntax", "None"], answer: 0 },
      { question: "State is?", options: ["Data", "Style", "HTML"], answer: 0 },
      { question: "Props are?", options: ["Inputs", "Outputs", "Loops"], answer: 0 }
    ],
    quiz2: [
      { question: "Hook is?", options: ["Function", "Class", "Loop"], answer: 0 },
      { question: "useState used for?", options: ["State", "API", "Loop"], answer: 0 },
      { question: "React DOM?", options: ["Rendering", "Database", "Server"], answer: 0 },
      { question: "Key prop?", options: ["Unique", "Loop", "Index"], answer: 0 },
      { question: "Virtual DOM?", options: ["Copy", "Real", "None"], answer: 0 }
    ]
  },

  4: {
    quiz1: [
      { question: "Node is?", options: ["Runtime", "Browser", "DB"], answer: 0 },
      { question: "NPM is?", options: ["Manager", "Language", "DB"], answer: 0 },
      { question: "Express is?", options: ["Framework", "DB", "Tool"], answer: 0 },
      { question: "FS module?", options: ["File", "Network", "UI"], answer: 0 },
      { question: "HTTP module?", options: ["Server", "UI", "DB"], answer: 0 }
    ],
    quiz2: [
      { question: "JSON is?", options: ["Format", "DB", "Code"], answer: 0 },
      { question: "require()?", options: ["Import", "Export", "Loop"], answer: 0 },
      { question: "Callback?", options: ["Function", "Loop", "Var"], answer: 0 },
      { question: "Async means?", options: ["Non-blocking", "Blocking", "Sync"], answer: 0 },
      { question: "Node uses?", options: ["V8", "Java", "Python"], answer: 0 }
    ]
  }

};