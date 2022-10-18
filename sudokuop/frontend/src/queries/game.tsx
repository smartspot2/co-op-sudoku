import { useQuery, useMutation } from "@tanstack/react-query";
import { HTTP_METHODS, fetchNormalized, fetchWithMethod } from "../utils/api";

interface GameInfoResponse {
    games: number[];
}

export const useGameInfo = () => {
    const query = useQuery<GameInfoResponse, Error>(["game", "info"], async () => {
        const response = await fetchNormalized("/game/info");
        const response_json = await response.json();
        if (response.ok) {
            return response_json;
        }

        throw new Error(`Error occurred while fetching game info: ${JSON.stringify(response_json)}`);
    });
    return query;
};

interface GameCreateRequest {
    usernames: string[];
}

interface GameCreateResponse {
    id: number;
}

export const useGameCreateMutation = () => {
    const mutation = useMutation<GameCreateResponse, Error, GameCreateRequest>(async (body: GameCreateRequest) => {
        const response = await fetchWithMethod("/game/create", HTTP_METHODS.POST, body);
        const response_json = await response.json();
        if (!response.ok) {
            throw new Error(`Error occurred while creating game: ${JSON.stringify(response_json)}`);
        }
        return response_json;
    });
    return mutation;
}
