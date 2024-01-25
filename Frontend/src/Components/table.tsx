import React, { useState } from 'react';
import { MyData } from '../Types/myData';

interface TableProps {
  myData: MyData[];
}

const Table: React.FC<TableProps> = ({ myData }) => {
  const [clickState, setClickState] = useState<{ [key: number]: boolean }>({});

  const [update, setUpdate] = useState({
    name: '',
    amount: 0,
    paid: 'false',
  });

  function handleClick(id: number | null) {
    console.log(id);
    setClickState((prevState) => ({
      ...prevState,
      [id!]: !prevState[id!],
    }));
  }

  function handleSave(id: number | null) {
    // fetch(`http://localhost:5500/sherehe/${id}`,{
    //     method:"PATCH",
    //     headers:{
    //         "Content-type":"Application/json"
    //     },
    //     body:JSON.stringify()

    // })
    console.log(update);
  }

  function handleInputChange(event: React.ChangeEvent<HTMLInputElement>) {
    const { name, value } = event.target;
    setUpdate((prevUpdate) => ({
      ...prevUpdate,
      [name]: value,
    }));
  }

  function handleSelectChange(event: React.ChangeEvent<HTMLSelectElement>) {
    const { name, value } = event.target;
    setUpdate((prevUpdate) => ({
      ...prevUpdate,
      [name]: value,
    }));
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4 [Poppins]">Birthday sherehe Details</h1>
      <table className="min-w-full border rounded overflow-hidden">
        <thead className="bg-gray-800 text-white">
          <tr>
            <th className="py-2 px-4">ID</th>
            <th className="py-2 px-4">Name</th>
            <th className="py-2 px-4">Amount</th>
            <th className="py-2 px-4">Paid</th>
            <th className="py-2 px-4">Update</th>
          </tr>
        </thead>
        <tbody>
          {myData.map((item) => (
            <tr key={item.id} className="bg-gray-100">
              <td className="py-2 px-4">{item.id}</td>
              <td>
                {clickState[item.id] ? (
                  <input
                    value={update.name}
                    type="text"
                    name="name"
                    placeholder={item.name}
                    onChange={handleInputChange}
                  />
                ) : (
                  <span>{item.name}</span>
                )}
              </td>
              <td>
                {clickState[item.id] ? (
                  <select name="amount" id="" onChange={handleSelectChange} value={update.amount}>
                    <option value={0}>0</option>
                    <option value={200}>200</option>
                  </select>
                ) : (
                  <span>{item.amount}</span>
                )}
              </td>
              <td>
                {clickState[item.id] ? (
                  <select name="paid" id="" onChange={handleSelectChange} value={update.paid}>
                    <option value="Paid">Paid</option>
                    <option value="Not paid">Not paid</option>
                  </select>
                ) : (
                  <span>{item.paid}</span>
                )}
              </td>
              <td className="py-2 px-4">
                {clickState[item.id] ? (
                  <button
                    onClick={() => handleSave(item.id)}
                    className="bg-red-600 p-2 rounded-lg hover:bg-red-400"
                  >
                    Save
                  </button>
                ) : (
                  <button
                    onClick={() => handleClick(item.id)}
                    className="bg-green-600 p-2 rounded-lg hover:bg-green-400"
                  >
                    Update
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Table;
