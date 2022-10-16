import React from 'react';
import * as ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import { Home } from "./Home";
import { Lobby } from "./Lobby";
import { Sudoku } from "./Sudoku";

const App = () => {
    const router = createBrowserRouter([
        {
            path: "/",
            element: <Home />
        },
        {
            path: "/game/lobby",
            element: <Lobby />
        },
        {
            path: "/game/play/:gameId",
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
