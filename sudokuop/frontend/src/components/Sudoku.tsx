import React, { useEffect, useState, useRef } from "react";
import { useParams } from "react-router-dom";

const BOARD: (number | null)[][] = [];
for (let i = 0; i < 9; i++) {
    BOARD.push([]);
    for (let j = 0; j < 9; j++) {
        BOARD[i].push(null);
    }
}

const CANDIDATES: boolean[][][] = [];
for (let i = 0; i < 9; i++) {
    CANDIDATES.push([]);
    for (let j = 0; j < 9; j++) {
        CANDIDATES[i].push([]);
        for (let k = 0; k < 9; k++) {
            CANDIDATES[i][j].push(false);
        }
    }
}

const VIEW: boolean[][] = [];
for (let i = 0; i < 9; i++) {
    VIEW.push([]);
    for (let j = 0; j < 9; j++) {
        VIEW[i].push(true);
    }
}

const KEYS = new Set(['1', '2', '3', '4', '5', '6', '7', '8', '9']);

export const Sudoku = () => {
    const [board, setBoard] = useState<number[][]>(BOARD);
    const [candidates, setCandidates] = useState<boolean[][][]>(CANDIDATES);
    const [view, setView] = useState<boolean[][]>(VIEW);
    const [pencilActive, setPencilActive] = useState<boolean>(false);

    const [socket, setSocket] = useState<WebSocket | null>(null);

    const pencilCheckbox = useRef<HTMLInputElement>();
    const { gameId } = useParams();

    // set up websocket
    useEffect(() => {
        const new_socket = new WebSocket(`ws://${window.location.host}/game/${gameId}/`);
        new_socket.onmessage = (e) => {
            const parsed = JSON.parse(e.data);
            // {board: ..., candidates: ...}
            const type = parsed["type"];
            if (type === "INIT") {
                const new_view = parsed["view"];
                const boolView = new_view.map(row => row.map(cell => cell ? true : false));
                setView(boolView);
            }
            const new_board = parsed["board"];
            const new_candidates = parsed["candidates"];
            const nullBoard = new_board.map(row => row.map(cell => cell === 0 ? null : parseInt(cell)));
            const boolCandidates = new_candidates.map(row => row.map(cell => cell.map(val => val ? true : false)));
            setBoard(nullBoard);
            setCandidates(boolCandidates);
        };
        // notify server that we've joined
        new_socket.onopen = () => {
            new_socket.send(JSON.stringify({ type: "START" }));
            setSocket(new_socket);
        };

        // close on cleanup
        return () => { new_socket.close() };
    }, []);

    const updateValue = (value: number, row_idx: number, col_idx: number) => {
        const new_board = board.map(row => row.slice());
        new_board[row_idx][col_idx] = value;
        const intBoard = new_board.map(row => row.map(cell => cell === null ? 0 : cell));
        const intCandidates = candidates.map(row => row.map(cell => cell.map(val => val ? 1 : 0)));
        const sentData = JSON.stringify({ type: "UPDATE", board: intBoard, candidates: intCandidates })
        console.log(sentData);
        socket.send(sentData);
    };

    const updateCandidate = (value: number, row_idx: number, col_idx: number) => {
        const new_candidates = candidates.map(row => row.map(vals => vals.slice()));
        new_candidates[row_idx][col_idx][value - 1] = !new_candidates[row_idx][col_idx][value - 1];
        const intCandidates = new_candidates.map(row => row.map(cell => cell.map(val => val ? 1 : 0)));
        const intBoard = board.map(row => row.map(cell => cell === null ? 0 : cell));
        const sentData = JSON.stringify({ type: "UPDATE", board: intBoard, candidates: intCandidates })
        console.log(sentData);
        socket.send(sentData);
    };

    const handlePencilActiveChange = () => {
        pencilCheckbox.current?.blur();
        setPencilActive(active => !active);
    }

    return <div className="sudoku-container">
        <div className="sudoku">
            <Board board={board} candidates={candidates} view={view} pencilActive={pencilActive} updateValue={updateValue} updateCandidate={updateCandidate} />
            <div className="menu">
                <label>
                    Pencil marks:
                    <input ref={pencilCheckbox} type="checkbox" checked={pencilActive} onChange={handlePencilActiveChange} />
                </label>
            </div>
        </div>
    </div>;
};

interface BoardProps {
    board: number[][];
    candidates: boolean[][][];
    view: boolean[][];
    pencilActive: boolean;

    updateValue: (value: number, row_idx: number, col_idx: number) => void;
    updateCandidate: (value: number, row_idx: number, col_idx: number) => void;
}
const Board = ({ board, candidates, view, pencilActive, updateValue, updateCandidate }: BoardProps): React.ReactElement => {
    const [selectedCell, setSelectedCell] = useState<number[]>([-1, -1]);

    const setSelectedCellWrapper = (newSelectedCell: number[]) => {
        // check to make sure that the new selected cell is actually visible
        if (view[newSelectedCell[0]][newSelectedCell[1]]) {
            setSelectedCell(newSelectedCell);
        } else {
            // otherweise, deselect
            setSelectedCell([-1, -1]);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        const [row_idx, col_idx] = selectedCell;
        let key: number;
        if (e.key === "Backspace") {
            key = null;
        } else if (KEYS.has(e.key)) {
            key = parseInt(e.key);
        } else {
            // ignore event
            return;
        }
        e.preventDefault();
        if (pencilActive) {
            // update candidate
            updateCandidate(key, row_idx, col_idx);
        } else {
            updateValue(key, row_idx, col_idx);
        }
    };

    /* parse a board into html */
    const parseBoard = (board: number[][], candidates: boolean[][][]): React.ReactNode => {
        const result = [];
        // (block_r, block_c) is the top-left cell
        for (let block_r = 0; block_r < 9; block_r += 3) {
            const block_row = [];
            for (let block_c = 0; block_c < 9; block_c += 3) {
                const block = [];
                for (let r = 0; r < 3; r++) {
                    const row = [];
                    for (let c = 0; c < 3; c++) {
                        row.push(<Cell
                            key={c}
                            value={board[block_r + r][block_c + c]}
                            candidates={candidates[block_r + r][block_c + c]}
                            selected={block_r + r === selectedCell[0] && block_c + c === selectedCell[1]}
                            visible={view[block_r + r][block_c + c]}

                            onClick={() => setSelectedCellWrapper([block_r + r, block_c + c])}
                            onKeyDown={handleKeyDown}
                        />);
                    }
                    block.push(<div className="board-block-row" key={r}>
                        {row}
                    </div>);
                }
                block_row.push(<div className="board-block" key={block_c}>
                    {block}
                </div>);
            }
            result.push(<div className="board-row" key={block_r}>
                {block_row}
            </div>);
        }
        return result;
    }

    const htmlBoard = parseBoard(board, candidates);
    return <div className="board" onBlur={() => setSelectedCell([-1, -1])}>
        {htmlBoard}
    </div>;
}

interface CellProps {
    value: number | null;
    candidates: boolean[];
    /* whether this cell is selected */
    selected: boolean;
    visible: boolean;

    /* set new selected cell */
    onClick: React.MouseEventHandler;
    onKeyDown: React.KeyboardEventHandler;
}

const Cell = ({ value, candidates, selected, visible, onClick, onKeyDown }: CellProps) => {
    let content = null;
    if (!visible) {
        content = null;
    } else if (value == null) {
        // no value; show candidates
        if (candidates.length > 0) {
            const candidate_block = [];
            for (let i = 0; i < 9; i += 3) {
                const candidate_row = [];
                for (let j = 0; j < 3; j++) {
                    let candidate_value = null;
                    if (candidates[i + j]) {
                        candidate_value = i + j + 1;
                    }
                    candidate_row.push(<div className="candidate-cell" key={j}>
                        {candidate_value}
                    </div>);
                }
                candidate_block.push(<div className="candidate-row" key={i}>
                    {candidate_row}
                </div>);
            }
            content = <div className="candidate-block">
                {candidate_block}
            </div>;
        } else {
            // no candidates; show nothing
        }
    } else {
        // show value
        content = <span className="board-cell-content">{value}</span>;
    }
    return <div className={`board-cell ${selected ? "selected" : ""} ${visible ? "" : "hidden"}`} onClick={onClick} onKeyDown={onKeyDown} tabIndex={0}>
        {content}
    </div>;
}
