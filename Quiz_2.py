#Dont have any IDE setup on my laptop as working on databricks these days. 
#Written a python class that works with the base functionality 
#And can be easily connected to an http end point when needed.
#I think it is more important to have a working test code that completes the functionality required

#One improvement that I added on the code below, In response error description.
#I added ability to return error descriptions in multiple languages


class Localized_Text:
  
  def __init__(self, language = "en-gb"):
    self.default_language = "en-gb"
    self.dictionary = self.Get_Dictionary(language)
    
  def Get_Dictionary(self, language):
  
    text_dictionary = {
      "en-gb": {
        "Quiz_Time": {
          "Is_Number_Multiple_By_7_9_Error_Code": "Expecting integer input"
        }
      },
      "fr": {
        "Quiz_Time": {
          "Is_Number_Multiple_By_7_9_Error_Code": "En attente d'une entrée entière"
        }
      }
    }

    if language not in text_dictionary:
      language = "en-gb"
    return text_dictionary[language]
  
class Quiz_Time:
  
  def __init__(self, localized_dictionary):    
    self.localized_dictionary = localized_dictionary
    
  #Expected input integer
  #If input is a multiple of 7, E is returned in the result object 
  #if input is a muliple of 9, E is returned in the result object
  #if input is a multiple of both 7 and 9, EG is returned in the result object
  #if input is not a valid integer, response code 422 is returned
  
  def Is_Number_Multiple_By_7_9(self, integer_input = None):
        
    if str(type(integer_input)) != "<class 'int'>":
      return {
        "responseCode": 422,
        "errorDescription": self.localized_dictionary["Quiz_Time"]["Is_Number_Multiple_By_7_9_Error_Code"],
        "result" : None
      }
    
    result = ""
    if integer_input % 7 == 0:
      result = "E"
      
    if integer_input % 9 == 0:
      result = result + "G"
    
    if result == "":
      result = str(integer_input)
    
    
    return {
      "responseCode": 200,
      "errorDescription": "",
      "result" : result
    } 
  
class Quiz_Time_Tests:
  
  def __init__(self):
    
      quizTime = Quiz_Time(Localized_Text().dictionary)
    
      result = quizTime.Is_Number_Multiple_By_7_9(7) 
      assert(result["responseCode"] == 200)
      assert(result["errorDescription"] == "")      
      assert(result["result"] == "E")
      
      assert(quizTime.Is_Number_Multiple_By_7_9(9)["result"] == "G")
      assert(quizTime.Is_Number_Multiple_By_7_9(9 * 7)["result"] == "EG")
      assert(quizTime.Is_Number_Multiple_By_7_9(9 * 7 + 1)["result"] == str(9 * 7 + 1))
      
      assert(quizTime.Is_Number_Multiple_By_7_9()["responseCode"] == 422)
      assert(quizTime.Is_Number_Multiple_By_7_9("Not an integer")["errorDescription"] == "Expecting integer input")
      
      quizTime = Quiz_Time(Localized_Text("fr").dictionary)
      assert(quizTime.Is_Number_Multiple_By_7_9(14.8)["errorDescription"] == "En attente d'une entrée entière")
  
Quiz_Time_Tests()
