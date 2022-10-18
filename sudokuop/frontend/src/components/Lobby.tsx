import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import { useGameCreateMutation, useGameInfo } from "../queries/game";

export const Lobby = () => {
    const [inviteUsernames, setInviteUsernames] = useState<string>("");
    const navigate = useNavigate();

    const { data: gameInfo, error: gameInfoError, status: gameInfoStatus } = useGameInfo();
    const [errorString, setErrorString] = useState<string>("");

    const gameCreateMutation = useGameCreateMutation();

    let currentGames = [];
    switch (gameInfoStatus) {
        case "error":
            setErrorString(`Error: ${gameInfoError.message}`);
            break;
        case "success":
            currentGames = gameInfo.games;
            break;
    }

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
        gameCreateMutation.mutate({ usernames: parsed }, {
            onSuccess: ({ id }) => {
                navigate(`/game/play/${id}`);
            }
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
        {errorString ?? <div className="error-test">{errorString}</div>}
        <div className="create-container">
            <h3>Create new game</h3>
            <label>Invite (comma-separated): <input className="invite-input" onChange={handleInviteChange} value={inviteUsernames} /></label>
            <button className="create-button" onClick={handleCreateGame} disabled={inviteUsernames.length == 0}>Create</button>
        </div>
    </div>;
};
