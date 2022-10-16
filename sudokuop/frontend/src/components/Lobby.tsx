import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { fetchJSON, fetchWithMethod, HTTP_METHODS } from "../utils/api";

export const Lobby = () => {
    const [currentGames, setCurrentGames] = useState<number[]>([]);
    const [inviteUsernames, setInviteUsernames] = useState<string>("");
    const navigate = useNavigate();

    useEffect(() => {
        // fetch the user's games
        fetchJSON("/game/info").then(data => {
            // format: {games: [id, ...]}
            console.log(data);
            setCurrentGames(data["games"] ?? []);
        });
    }, []);

    const handleJoinGame = (id: number) => {
        navigate(`/game/play/${id}`);
    };

    const handleInviteChange = (e) => {
        const val: string = e.target.value;
        setInviteUsernames(val);
    };

    const handleCreateGame = () => {
        const parsed = inviteUsernames.split(",")
            .map(username => username.trim())
            .filter(username => username.length > 0);
        fetchWithMethod("/game/create", HTTP_METHODS.POST, {
            usernames: parsed
        }).then(response => response.json())
            .then((data) => {
                const id = data.id;
                navigate(`/game/play/${id}`)
            });
    }

    return <div className="lobby-container">
        {currentGames?.length > 0 &&
            <div className="join-container">
                <h3>Join Game</h3>
                <div className="join-list">
                    {currentGames.map(gameId =>
                        <button key={gameId} className="join-button" onClick={() => handleJoinGame(gameId)}>
                            Join (id {gameId})
                        </button>
                    )}
                </div>
            </div>
        }
        <div className="create-container">
            <h3>Create new game</h3>
            <label>Invite (comma-separated): <input className="invite-input" onChange={handleInviteChange} value={inviteUsernames} /></label>
            <button className="create-button" onClick={handleCreateGame} disabled={inviteUsernames.length == 0}>Create</button>
        </div>
    </div>;
};
