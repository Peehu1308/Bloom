import React from 'react';
import Box_grid from './box_grid';

export const Plants_screen = () => {
  return (
    <div className='w-full min-h-screen bg-gray-50'>

      <div className='relative bg-green-800 w-full p-8 md:p-16 text-white flex flex-col items-start justify-center'>
        

        <h1 className='text-4xl sm:text-5xl md:text-6xl font-bold mb-6 leading-snug'>
          Discover the Flowers of the World
        </h1>

        <p className='text-lg sm:text-xl mb-6'>
          Explore, learn, and admire the beauty of plants from every corner of the globe.
        </p>
        
        <button className='bg-white text-green-900 font-semibold px-8 py-3 rounded-lg shadow-lg hover:bg-green-50 transition duration-300'>
          Discover Now
        </button>


        <div className='absolute right-0 bottom-0 w-72 h-72 bg-green-700 rounded-full opacity-30 -z-10'></div>
      </div>

      <div className='p-6 md:p-12'>
        <Box_grid />
      </div>
    </div>
  );
};
