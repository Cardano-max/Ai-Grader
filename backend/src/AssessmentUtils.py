from src.GPTUtils import get_assessment
from config import storageManager
from src.database.Assessments import Assessments, db
from src.utils.parsers import parse_file

def get_response_for_single_assessment(identity, assessment_file, request_data):
    try:
        assessment_filepath = ""
        if assessment_file:
            if not assessment_file.filename.lower().endswith((".docx", ".pdf")):
                return "Please select a valid file", 400
            assessment_filepath = "static/temp/" + assessment_file.filename
            assessment_file.save(assessment_filepath)
            
            request_data['sample_of_work'] = parse_file(assessment_filepath)

        

        context_country = 'Australia'
        context_curriculum = 'Australian Curriculum'
        context_subject = request_data['assessment_setup'].get("subject")
        context_year_level = request_data['class_details'].get("year_level")
        
        criteria = request_data['assessment_setup'].get("criteria")
        checks = request_data['assessment_setup'].get("checks")
        feedback = request_data['assessment_setup'].get("feedback")
        
        
        
        work_sample = request_data.get("sample_of_work")


        model = request_data['ai_settings'].get('model')
        max_tokens = request_data['ai_settings'].get('max_response')
        temperature = request_data['ai_settings'].get('temperature')
        top_p = request_data['ai_settings'].get('top_p')
        frequency_penalty = request_data['ai_settings'].get('frequency_penalty')
        presence_penalty = request_data['ai_settings'].get('presence_penalty')

        

        completion, response = get_assessment(feedback, context_country, context_year_level, context_subject,
                            context_curriculum, criteria, checks, work_sample, model, temperature, max_tokens, frequency_penalty, 
                            top_p)

        rows = response.split("\n")
        score_text = ""
        if len(rows) > 1:
            score_text = "".join([t for t in rows[-1] if t.isnumeric()])

        score = -1
        try:
            if score_text != "":
                score = int(score_text)
        except:
            pass
        #print(response)
        #int(response.split("\n")[-1].split(":")[-1].strip())
        files = None
        if assessment_filepath != "":
            resp = storageManager.upload_blob_and_return_meta(assessment_filepath, f"files/{identity}", public=True, delete=True, random_name=True)
            files = [resp]

        # Save input and output to Pairs table
        pair = Assessments(
            user_id=identity,
            context_country=context_country,
            context_curriculum=context_curriculum,
            context_subject=context_subject,
            context_year_level=int(context_year_level) if context_year_level.isnumeric() else None,
            work_sample=work_sample, 
            criteria=criteria,
            evaluation_response=response,
            checks=checks,
            model=model,
            feedback=feedback,
            max_tokens=max_tokens,
            token_count = completion.usage.total_tokens,
            top_p = top_p,
            temperature = temperature,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            response_status=200,
            score=score,
            files=files,
            student_name=request_data['class_details'].get("student_name") if assessment_filepath == "" else assessment_filepath.split("/")[-1].split(".")[0],
            course_title=request_data['class_details'].get("course_title"),
            assessment_title=request_data['class_details'].get("assessment_title")
        )
        #db.session.add(pair)
        #db.session.commit()


        return {
            'pair' : pair,
            'evaluation_comments' : response,
            'text' : work_sample,
            'filename' : assessment_filepath.split("/")[-1],
            'id' : pair.id
        }, 200
    except Exception as ex:
        return str(ex), 400