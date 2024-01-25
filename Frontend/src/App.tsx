import { useState, useEffect } from 'react';
import Table from './Components/table';
import { MyData } from './Types/myData';
import './App.css';

function App() {
  const [data, setData] = useState<MyData[]>([]);

  function fetching() {
    fetch('http://localhost:5500/sherehe', {
      method: 'GET',
      headers: {
        'Content-type': 'Application/json',
      },
    })
      .then((resp) => resp.json())
      .then((data) => {
        console.log(data);
        setData(data);
      });
  }

  useEffect(() => {
    fetching();
  }, []);

  return (
    <>
      <Table myData={data} setMyData={setData} func={fetching} />
    </>
  );
}

export default App;
