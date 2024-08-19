import { BrowserRouter as Router, Route } from 'react-router-dom';
import { Provider } from 'react-redux';
import { createStore } from 'redux';
import rootReducer from './reducers';
import TodoList from './components/TodoList';

const store = createStore(rootReducer);

function App() {
  return (
    <Provider store={store}>
      <Router>
        <Route path="/" component={TodoList} />
      </Router>
    </Provider>
  );
}

export default App;