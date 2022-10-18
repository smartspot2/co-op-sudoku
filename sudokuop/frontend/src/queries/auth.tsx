import { useMutation } from "@tanstack/react-query";
import { fetchWithMethod, HTTP_METHODS } from "../utils/api";

interface AuthResponse {
    ok: boolean;
    json: {
        error: string;
    };
}

export const useLoginMutation = () => {
    const mutation = useMutation<AuthResponse, Error, string>(async (username: string) => {
        const response = await fetchWithMethod("login", HTTP_METHODS.POST, {
            username: username
        });
        const response_json = await response.json();
        return { ok: response.ok, json: response_json };
    });
    return mutation;
}

export const useRegisterMutation = () => {
    const mutation = useMutation<AuthResponse, Error, string>(async (username: string) => {
        const response = await fetchWithMethod("register", HTTP_METHODS.POST, {
            username: username
        });
        const response_json = await response.json();
        return { ok: response.ok, json: response_json };
    });
    return mutation;
}
