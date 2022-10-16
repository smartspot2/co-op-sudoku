import React from 'react';
import * as ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import { Home } from "./Home";
import { Sudoku } from "./Sudoku";

const App = () => {
    const router = createBrowserRouter([
        {
            path: "/",
            element: <Home />
        },
        {
            path: "/game",
            element: <Sudoku />
        }
    ]);

    return <React.StrictMode>
        <RouterProvider router={router} />
    </React.StrictMode>;
};
export default App;

const root = ReactDOM.createRoot(document.getElementById("app"));
root.render(<App />);
