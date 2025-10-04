// Conservation_screen.jsx
import React from 'react'
import Conservation_box from './conservation_box'
import { conservationData } from '../data/conservationData'

export const Conservation_screen = () => {
  return (
    <div className="min-h-screen bg-black px-6 py-10">
      
      {/* Header Section */}
      <div className='max-w-6xl mx-auto mb-8'>
        <h1 className='text-white text-4xl md:text-5xl font-extrabold'>
          Conservation Recommendations
        </h1>
        <p className='text-green-200 mt-2'>
          Sustainable actions for ecosystem protection and resource resilience.
        </p>
      </div>

      {/* Grid Section */}
      <div className='max-w-6xl mx-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6'>
        {conservationData.map((item, index) => (
          <Conservation_box key={index} {...item} />
        ))}
      </div>
    </div>
  )
}
