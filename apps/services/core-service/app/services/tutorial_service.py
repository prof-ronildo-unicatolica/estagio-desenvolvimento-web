from sqlalchemy.orm import Session

from app.repositories.tutorial_repository import TutorialRepository


class TutorialService:
    def __init__(self, db: Session):
        self.repository = TutorialRepository(db)

    def get_sobre_data(self) -> dict:
        professores = self.repository.get_professor_with_details()
        stacks = self.repository.get_stacks_with_tecnologias()

        equipe_info = {
            "equipe": "Alpha",
            "ano": 2026,
            "semestre": 2,
            "professor": None,
            "disciplinas": [],
            "stacks": [],
        }

        if professores:
            prof = professores[0]
            equipe_info["professor"] = {
                "nome": prof.nome,
                "email": prof.email,
                "sala": prof.detalhe.sala if prof.detalhe else "",
                "biografia": prof.detalhe.biografia if prof.detalhe else "",
                "biografia_mapa": prof.detalhe.biografia_mapa
                if (prof.detalhe and prof.detalhe.biografia_mapa)
                else None,
            }
            for disc in prof.disciplinas:
                equipe_info["disciplinas"].append(
                    {
                        "nome": disc.nome,
                        "ano": disc.ano,
                        "semestre": disc.semestre,
                        "tecnologias": [t.nome for t in disc.tecnologias],
                    }
                )

        for st in stacks:
            stack_data = {"nome": st.nome, "tecnologias": []}
            for tech in st.tecnologias:
                stack_data["tecnologias"].append(
                    {
                        "nome": tech.nome,
                        "linguagens": [lang.nome for lang in tech.linguagens],
                    }
                )
            equipe_info["stacks"].append(stack_data)

        return equipe_info

    def get_professor_by_id(self, professor_id):
        return self.repository.get_professor_by_id(professor_id)

    def create_professor(self, payload):
        return self.repository.create_professor(
            nome=payload.nome,
            email=payload.email,
            sala=payload.sala,
            biografia=payload.biografia,
            biografia_mapa=payload.biografia_mapa,
        )
