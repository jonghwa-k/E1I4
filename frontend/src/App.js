import React, { useEffect, useState } from 'react';
import axios from 'axios';
import CustomNavbar from './CustomNavbar';

function App() {
  // 상태 변수 설정
  const [message, setMessage] = useState('');

  // 컴포넌트가 마운트될 때 Django API 호출
  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/hello/')  // Django API 주소
      .then(response => {
        setMessage(response.data.message);  // Django API에서 받아온 메시지를 상태로 설정
      })
      .catch(error => {
        console.error('There was an error!', error);
      });
  }, []);

  // return (
  //   <div className="App">
  //     <header className="App-header">
  //       <h1>{message}</h1>  {/* API에서 받아온 메시지 표시 */}
  //       <p>
  //         This is a message from Django API.
  //       </p>
  //     </header>
  //   </div>
  // );
  return (
    <div>
      <CustomNavbar />
      <h1>TRESS</h1>
    </div>
  )
}

export default App;
