package login;

import entity.User;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;

public class Test extends HttpServlet {
    @Override
    protected void doPost(HttpServletRequest req) {
        String username = req.getParameter("username");
        String password = req.getParameter("password");
        User user = new User();
        user.setUsername(username);
        user.setPassword(password);
        req.getSession().setAttribute("user", user);
    }
}
