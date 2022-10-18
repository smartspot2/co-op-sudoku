import React, { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

import { useLoginMutation, useRegisterMutation } from "../queries/auth";

export const Home = () => {
    const loginUsername = useRef<HTMLInputElement>();
    const [loginError, setLoginError] = useState<string>("");
    const registerUsername = useRef<HTMLInputElement>();
    const [registerError, setRegisterError] = useState<string>("");

    const navigate = useNavigate();

    const loginMutation = useLoginMutation();
    const registerMutation = useRegisterMutation();

    // log in an existing user
    const login = () => {
        const username = loginUsername.current?.value;
        if (!username) {
            setLoginError("Please enter a username.");
            return;
        }
        loginMutation.mutate(username, {
            onSuccess: ({ ok, json }) => {
                if (!ok) {
                    setLoginError(json.error);
                } else {
                    navigate("/game/lobby");
                }
            }
        });
    };

    // register a new user
    const register = () => {
        const username = registerUsername.current?.value;
        if (!username) {
            setRegisterError("Please enter a username.");
            return;
        }
        registerMutation.mutate(username, {
            onSuccess: ({ ok, json }) => {
                if (!ok) {
                    setRegisterError(json.error);
                } else {
                    navigate("/game/lobby");
                }
            }
        });
    };

    return <div className="home-container">
        <div className="login-container">
            <h3 className="login-header">Login</h3>
            <label className="username-input">Username: <input ref={loginUsername} /></label>
            <span className="home-error">{loginError}</span>
            <button className="home-btn" onClick={login}>Login</button>
        </div>
        <div className="register-container">
            <h3 className="register-header">Register</h3>
            <label className="username-input">Username: <input ref={registerUsername} /></label>
            <span className="home-error">{registerError}</span>
            <button className="home-btn" onClick={register}>Register</button>
        </div>
    </div>
}
