from .models import User

def validate_user_data(user_data):
    
        username = user_data.get("username")
        password = user_data.get("password")
        name = user_data.get("name")
        email = user_data.get("email")
        nickname = user_data.get("nickname")  
        bio = user_data.get("bio")

        if len(nickname) > 15:
            return "닉네임은 15글자 이하여야 합니다."
        
        if len(password) < 8:
            return "비밀번호를 8글자 이상 입력해주세요."
        
        if User.objects.filter(username=username).exists():
            return "이미 존재하는 아이디입니다."
        
        if User.objects.filter(nickname=nickname).exists():
            return "이미 존재하는 닉네임입니다."
        
        if not name:
            return "이름을 필수로 입력해주세요!"