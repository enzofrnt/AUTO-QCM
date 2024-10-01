from .custom_error_view import (
    custom_page_not_found_view,
    custom_permission_denied_view,
    custom_server_error_view,
)
from .qcm.delete_multiple_qcms_view import delete_multiple_qcms
from .dashboard.enseignant_dashboard_view import enseignant_dashboard
from .dashboard.etudiant_dashboard_view import etudiant_dashboard
from .export_view import export_qcm_latex, export_qcm_xml, export_question_xml
from .home_view import home
from .login_view import CustomLoginView
from .qcm.qcm_answer_view import repondre_qcm
from .qcm.qcm_correction_view import corriger_qcm
from .qcm.qcm_create_or_edit_view import create_or_edit_qcm
from .qcm.qcm_delete_view import delete_qcm
from .qcm.qcm_list_view import QcmListView
from .dashboard.qcm_statistique_view import qcm_statistics
from .question.question_create_or_edit_view import create_or_edit_question
from .question.question_delete_view import delete_question
from .question.question_generation_view import question_generation_view
from .question.question_list_view import QuestionListView
from .remove_tags_view import remove_tag
from .dashboard.reponse_qcm_dashboard_view import qcm_responses
from .question.save_generated_questions_view import save_generated_questions
from .dashboard.search_students_view import search_student
from .support_doc_view import support_doc
