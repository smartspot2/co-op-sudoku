import React from 'react';
import * as ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

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

    const queryClient = new QueryClient();

    return <React.StrictMode>
        <QueryClientProvider client={queryClient}>
            <RouterProvider router={router} />
        </QueryClientProvider>
    </React.StrictMode>;
};
export default App;

const root = ReactDOM.createRoot(document.getElementById("app"));
root.render(<App />);
