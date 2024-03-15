package pyiom;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.*;
import com.sas.iom.SAS.ILanguageService;

public class cancel implements Runnable 
   {
   private Socket sc;
   private ILanguageService    lang    = null;


   public cancel(Socket sc, ILanguageService lang)
      {
      this.sc   = sc;
      this.lang = lang;
      }


   public void run()
      {
      InputStreamReader inc;
      int            op;

      try 
         {
         inc = new InputStreamReader(this.sc.getInputStream());
         }
      catch (IOException e2) 
         {
         return;
         }

      while(true)
         {
         try
            {
            op  = inc.read();
            if (op == 'C')
               try
                  {
                  lang.Async(true);
                  lang.Cancel();
                  lang.Async(false);
                  }
               catch (org.omg.CORBA.OBJECT_NOT_EXIST e1)
                  {
                  return;
                  }
            else
               return;
            }
         catch (IOException e)
            {
            return;
            }
         catch (Exception e)
            {
            return;
            }
         catch (Error e)
            {
            return;
            }
         }
      }   
   }
