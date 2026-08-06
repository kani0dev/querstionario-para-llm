from src.app.controller.auth_controler import router as auth
from src.app.controller.studant_controller import router as student_router
from src.app.controller.teacher_controller import router as teacher_router

routers = [
    student_router,
    teacher_router,
    auth
    ]
