import React, { useEffect, useState } from 'react'
import Box from './box_plants';

const Box_grid = () => {
    const [plants,setPlants]=useState([]);

    useEffect(()=>{
        fetch('/train_plants.json')
        .then(res=>res.json())
        .then(data=>setPlants(data))
        .catch(err=>console.error(err))
    },[]);

  return (
    <div className='grid grid-cols-4 justify-evenly gap-5 p-3 m-4'>{plants.map((plant,index)=>(
        <Box key={index} plant={plant}/>
    ))}</div>
  )
}

export default Box_grid