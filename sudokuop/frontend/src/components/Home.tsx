import React, { useRef, useState } from "react";
import { fetchWithMethod, HTTP_METHODS } from "../utils/api";

export const Home = () => {
    const loginUsername = useRef<HTMLInputElement>();
    const [loginError, setLoginError] = useState<string>("");
    const registerUsername = useRef<HTMLInputElement>();
    const [registerError, setRegisterError] = useState<string>("");

    const login = () => {
        const username = loginUsername.current?.value;
        if (!username) {
            setLoginError("Please enter a username.");
            return;
        }
        fetchWithMethod("login", HTTP_METHODS.POST, {
            username: username
        }).then(response => {
            // TODO: handle error
            return response.json()
        }).then(handleResponseData);
    };

    const register = () => {
        const username = registerUsername.current?.value;
        if (!username) {
            setRegisterError("Please enter a username.");
            return;
        }
        fetchWithMethod("register", HTTP_METHODS.POST, {
            username: username
        }).then(response => {
            // TODO: handle error
            return response.json()
        }).then(handleResponseData);
    };

    const handleResponseData = (data) => {
        // Response data: TODO
    }

    return <div className="home-container">
        <div className="login-container">
            <h3 className="login-header">Login</h3>
            <label className="username-input">Username: <input ref={loginUsername} /></label>
            <button className="home-btn" onClick={login}>Login</button>
        </div>
        <div className="register-container">
            <h3 className="register-header">Register</h3>
            <label className="username-input">Username: <input ref={registerUsername} /></label>
            <button className="home-btn" onClick={register}>Register</button>
        </div>
    </div>
}
