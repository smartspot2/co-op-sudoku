import React from 'react';
import * as ReactDOM from 'react-dom/client';

const App = () => {
    return <div>Test app</div>;
};
export default App;

const root = ReactDOM.createRoot(document.getElementById("app"));
root.render(<App />);
