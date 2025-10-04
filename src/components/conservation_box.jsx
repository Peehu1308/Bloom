// Conservation_box.jsx
import React, { useState } from 'react'

const Conservation_box = ({ image, type, title, data, region, threatLevel, details }) => {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <div className='border border-gray-200 rounded-xl shadow-md flex flex-col overflow-hidden hover:shadow-lg transition'>
        <img src={image} alt={title} className='w-full h-40 object-cover' />

        <div className='p-4 flex flex-col flex-1'>
          <p className='text-lg font-bold text-center'>{title}</p>

          <button className='mt-2 px-3 py-1 bg-green-700 text-white rounded-md text-xs self-start'>
            {type}
          </button>

          <p className='text-gray-600 text-sm mt-2 flex-1'>{data}</p>

          <p className='text-sm mt-1'><strong>Region:</strong> {region}</p>
          <p className='text-sm mt-1'>
            <strong className='text-red-700'>Threat Level:</strong> {threatLevel}
          </p>
        </div>

        {/* Fixed Button at Bottom */}
        <div className='p-4 bg-black'>
          <button
            className='w-full py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md'
            onClick={() => setIsOpen(true)}
          >
            View Details
          </button>
        </div>
      </div>

      {/* Modal */}
      {isOpen && (
        <div className='fixed inset-0 flex items-center justify-center bg-black/50 z-50'>
          <div className='bg-black w-full max-w-md p-6 rounded-lg shadow-xl relative'>
            <h2 className='text-xl font-bold mb-2'>{title}</h2>
            <p className='text-sm text-gray-400 mb-4'>{details}</p>

            <button
              className='absolute top-2 right-2 text-gray-500 hover:text-black'
              onClick={() => setIsOpen(false)}
            >
              ✕
            </button>
          </div>
        </div>
      )}
    </>
  )
}

export default Conservation_box
