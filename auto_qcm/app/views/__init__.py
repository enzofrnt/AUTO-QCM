from .admin_dasboard_view import custom_admin_view
from .change_password_view import change_password_view
from .custom_error_view import (
    cause_server_error,
    custom_page_not_found_view,
    custom_permission_denied_view,
    custom_server_error_view,
)
from .delete_multiple_qcms_view import delete_multiple_qcms
from .delete_tag_view import delete_tag
from .enseignant_dashboard_view import enseignant_dashboard
from .etudiant_dashboard_view import etudiant_dashboard
from .export_view import (
    export_qcm_amctxt,
    export_qcm_latex,
    export_qcm_xml,
    export_question_xml,
)
from .home_view import home
from .import_view import import_questions
from .login_view import CustomLoginView
from .qcm_acces_view import acces_qcm
from .qcm_answer_view import repondre_qcm
from .qcm_correction_view import corriger_qcm
from .qcm_create_or_edit_view import create_or_edit_qcm
from .qcm_delete_view import delete_qcm
from .qcm_list_view import QcmListView
from .qcm_statistique_view import qcm_statistics
from .question_create_or_edit_view import create_or_edit_question
from .question_delete_view import delete_question
from .question_duplicate_view import duplicate_question
from .question_generation_view import question_generation_view
from .question_list_view import QuestionListView
from .remove_tags_view import remove_tag
from .reponse_qcm_dashboard_view import qcm_responses
from .save_generated_questions_view import save_generated_questions
from .search_students_view import search_student
from .support_doc_view import support_doc
