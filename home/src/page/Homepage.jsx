import React from 'react';
import Connection from '../components/Connection';
import Header from '../components/Headers';
import Footer from '../components/Footer';
import Heros from '../components/Heros';

function HomePage() {
    return (
        <div className='HomePage'>
            <Header />
            <Heros />
            <Footer />
            <Connection />
        </div>
    );
  }
  
  export default HomePage;
