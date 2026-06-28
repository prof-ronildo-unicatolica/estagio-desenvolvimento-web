export default function Sidebar() {
  return (
    <div className="bg-dark text-white p-3 rounded shadow-sm h-100">
      <h5 className="text-primary fw-bold mb-4 border-bottom pb-2">Menu Tutorial</h5>
      <ul className="nav nav-pills flex-column mb-auto">
        <li className="nav-item mb-2">
          <a href="#" className="nav-link text-white active" aria-current="page">
            Inicio
          </a>
        </li>
        <li className="nav-item mb-2">
          <a href="#professor-profile" className="nav-link text-white">
            1. Perfil do Professor
          </a>
        </li>
        <li className="nav-item mb-2">
          <a href="#disciplinas-list" className="nav-link text-white">
            2. Disciplinas e Techs
          </a>
        </li>
        <li className="nav-item mb-2">
          <a href="#stacks-table" className="nav-link text-white">
            3. Stacks e Linguagens
          </a>
        </li>
        <li className="nav-item mb-2">
          <a href="#image-carousel" className="nav-link text-white">
            4. Carousel e Imagem
          </a>
        </li>
      </ul>
    </div>
  );
}
