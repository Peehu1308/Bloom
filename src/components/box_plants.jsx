import React from 'react';

const Box = ({ plant }) => {
  return (
    <div className="bg-white border border-gray-200 rounded-2xl shadow-lg overflow-hidden w-64 hover:scale-105 transform transition duration-300">
      

      <div className="h-48 w-full bg-gray-100 flex items-center justify-center">
        {plant.photos ? (
          <img
            src={plant.photos}
            alt={plant.species_guess}
            className="h-full w-full object-cover"
          />
        ) : (
          <span className="text-gray-400">No Image</span>
        )}
      </div>


      <div className="p-4">
        <p className="text-lg font-semibold text-gray-800 truncate">{plant.species_guess}</p>
        {/* {plant.quality_grade && (
          <p className="text-sm text-gray-500 mt-1">{plant.quality_grade}</p>
        )} */}
      </div>
    </div>
  );
};

export default Box;
