TAILWIND_CONFIG = """/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {},
    },
    plugins: [],
};
"""

POSTCSS_CONFIG = """/** @type {import('postcss').ProcessOptions} */
export default {
    plugins: {
        tailwindcss: {},
        autoprefixer: {},
    },
};
"""

APP_CSS_CONTENT = """@tailwind base;
@tailwind components;
@tailwind utilities;
"""

APP_JSX_CONTENT = """function App() {
    return (
        <>
            <h1 className="text-xl font-bold bg-blue-500 text-white">Testando o Tailwind</h1>
        </>
    );
}

export default App;
"""

MAIN_JSX_CONTENT = """import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import './App.css';

const root = createRoot(document.getElementById('root'));
root.render(
    <StrictMode>
        <App />
    </StrictMode>,
);
"""