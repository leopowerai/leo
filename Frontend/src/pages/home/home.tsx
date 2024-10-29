function Home() {
    return (
      <div className="min-h-screen bg-primary p-8">
        <div className="max-w-4xl mx-auto">
          {/* Logo en la esquina superior */}
          <div className="w-24 mb-8">
            <svg fill="none" viewBox="0 0 92 32" xmlns="http://www.w3.org/2000/svg">
              {/* El mismo SVG que usamos en App.tsx */}
              <g fill="#0AE98A" clipPath="url(#platzi-logo-new_svg__a)">
                {/* ... paths del SVG ... */}
              </g>
              <defs>
                <clipPath id="platzi-logo-new_svg__a">
                  <path fill="#fff" d="M.461 0h91.077v32H.461z"/>
                </clipPath>
              </defs>
            </svg>
          </div>
          
          <div className="bg-[#1E1E1E] rounded-lg p-8 shadow-lg">
            <h1 className="text-3xl text-white font-bold mb-6">
              Bienvenido a Leo
            </h1>
            
            <div className="grid gap-6">
              <div className="bg-[#2D2D2D] p-6 rounded-lg">
                <h2 className="text-xl text-white mb-4">Información del Usuario</h2>
                <div className="space-y-3">
                  <p className="text-gray-300">
                    <span className="font-semibold">Usuario:</span> {localStorage.getItem('username')}
                  </p>
                  <p className="text-gray-300">
                    <span className="font-semibold">GitHub:</span>{' '}
                    <a 
                      href={localStorage.getItem('githubUrl') || '#'} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-green-400 hover:text-green-300"
                    >
                      {localStorage.getItem('githubUrl')}
                    </a>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
  
  export default Home;