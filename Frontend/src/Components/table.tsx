import React, { useState, useEffect } from 'react';
import { MyData } from '../Types/myData';

interface TableProps {
  myData: MyData[];
  setMyData: React.Dispatch<React.SetStateAction<MyData[]>>; 
  func: () => void;
}

const Table: React.FC<TableProps> = ({ myData, setMyData,func }) => {
    const [clickState, setClickState] = useState<{ [key: number]: boolean }>({});

    const [update, setUpdate] = useState({
      name: '',
      amount: 0,
      paid: 'Paid',
    });
  
    // Add state variables for totalPaid, totalNotPaid, and totalAmount
    const [totalPaid, setTotalPaid] = useState(0);
    const [totalNotPaid, setTotalNotPaid] = useState(0);
    const [totalAmount, setTotalAmount] = useState(0);
  
    useEffect(() => {
      // Update the 'update' state whenever myData changes
      setUpdate({
        name: '',
        amount: 0,
        paid: 'Paid',
      });
  
      // Calculate totals whenever myData changes
      const paidCount = myData.filter((item) => item.paid === 'Paid').length;
      const notPaidCount = myData.filter((item) => item.paid === 'Not paid').length;
      const total = myData.reduce((sum, item) => sum + item.amount, 0);
  
      setTotalPaid(paidCount);
      setTotalNotPaid(notPaidCount);
      setTotalAmount(total);
    }, [myData]);
  
    function handleClick(id: number | null) {
      console.log(id);
      setClickState((prevState) => ({
        ...prevState,
        [id!]: !prevState[id!],
      }));
    }
  
    async function handleSave(id: number | null) {
      try {
        const response = await fetch(`http://localhost:5500/sherehe/${id}`, {
          method: 'PATCH',
          headers: {
            'Content-type': 'application/json',
          },
          body: JSON.stringify(update),
        });
  
        if (!response.ok) {
          throw new Error(`Failed to update data for ID ${id}`);
        }
  
        // Update the state with the latest data
        const updatedData = await response.json();
        setClickState((prev) => ({
          ...prev,
          [id!]: !prev[id!],
        }));
        func();
        console.log(updatedData, 'Status updated');
      } catch (error) {
        console.error('Error updating data:', error);
      }
    }
  
    async function handleDelete(id: number | null) {
      try {
        const response = await fetch(`http://localhost:5500/sherehe/${id}`, {
          method: 'DELETE',
        });
  
        if (!response.ok) {
          throw new Error(`Failed to delete data for ID ${id}`);
        }
  
        // Update the state by removing the deleted row
        setMyData((prevMyData) => prevMyData.filter((item) => item.id !== id));
        func();
        console.log(`Row with ID ${id} deleted`);
      } catch (error) {
        console.error('Error deleting data:', error);
      }
    }
  
    async function handleAddUser() {
      try {
        const response = await fetch('http://localhost:5500/sherehe', {
          method: 'POST',
          headers: {
            'Content-type': 'application/json',
          },
          body: JSON.stringify({}), // Send an empty object for a new user
        });
  
        if (!response.ok) {
          throw new Error('Failed to add a new user');
        }
  
        // Update the state with the latest data
        const newUser = await response.json();
        setMyData((prevMyData) => [...prevMyData, newUser]);
        setClickState((prev) => ({
          ...prev,
          [newUser.id!]: true, // Open the new user for editing
        }));
      } catch (error) {
        console.error('Error adding a new user:', error);
      }
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
      <button onClick={handleAddUser} className="bg-blue-500 text-white p-2 rounded-md mb-4">
        Add User
      </button>
      
      <table className="min-w-full border rounded overflow-hidden">
        <thead className="bg-gray-800 text-white">
          <tr>
            <th className="py-2 px-4">ID</th>
            <th className="py-2 px-4">Name</th>
            <th className="py-2 px-4">Amount</th>
            <th className="py-2 px-4">Paid</th>
            <th className="py-2 px-4">Actions</th>
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
                  <select
                    name="paid"
                    id=""
                    onChange={handleSelectChange}
                    value={update.paid}
                  >
                    <option value="Paid">Paid</option>
                    <option value="Not paid">Not paid</option>
                  </select>
                ) : (
                  <span>{item.paid}</span>
                )}
              </td>
              <td className="py-2 px-4">
                {clickState[item.id] ? (
                  <>
                    <button
                      onClick={() => handleSave(item.id)}
                      className="bg-red-600 p-2 rounded-lg hover:bg-red-400 mr-2"
                    >
                      Save
                    </button>
                    <button
                      onClick={() => handleDelete(item.id)}
                      className="bg-gray-600 p-2 rounded-lg hover:bg-gray-400"
                    >
                      Delete
                    </button>
                  </>
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
            <div className="flex justify-center">
        <div className="bg-gray-200 p-4 m-2 rounded-md shadow-md">
            <p className="text-lg font-semibold">Total Paid: {totalPaid}</p>
        </div>
        <div className="bg-gray-200 p-4 m-2 rounded-md shadow-md">
            <p className="text-lg font-semibold">Total Not Paid: {totalNotPaid}</p>
        </div>
        <div className="bg-gray-200 p-4 m-2 rounded-md shadow-md">
            <p className="text-lg font-semibold">Total Amount Paid: {totalAmount}</p>
        </div>
</div>

         

    </div>
  );
};

export default Table;
