package pyiom;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.*;
import com.sas.iom.SAS.ILanguageService;
import com.sas.iom.SASIOMDefs.GenericError;
import com.sas.services.connection.ConnectionInterface;

public class cancel implements Runnable 
   {
   private int port;
   private String addr;
   private ConnectionInterface cx      = null;
   private ILanguageService    lang    = null;


   public cancel(String addr, int port, ConnectionInterface cx, ILanguageService lang)
      {
      this.addr = addr;
      this.port = port;
      this.cx   = cx;
      this.lang = lang;
      }


   public void run()
      {
      InputStreamReader inc;
      Socket         sc = null;
      int            op;

      try
         {
         sc  = new Socket(this.addr, this.port);
         }
      catch (IOException e)
         {
         e.printStackTrace();
         }

      while(true)
         {
         try
            {
            inc = new InputStreamReader(sc.getInputStream());
            op  = inc.read();
            if (op == 'C')
               try
                  {
                  lang.Async(true);
                  lang.Cancel();
                  lang.Async(false);
                  }
               catch (GenericError e1)
                  {
                  }
            else
               return;
            }
         catch (Exception e)
            {
            try
               {
               lang.Async(true);
               lang.Cancel();
               lang.Async(false);
               }
            catch (GenericError e1)
               {
               }
            cx.close();
            try
               {
               sc.close();
               }
            catch (IOException e1)
               {
               }
            return;
            }
         catch (Error e)
            {
            try
               {
               lang.Async(true);
               lang.Cancel();
               lang.Async(false);
               }
            catch (GenericError e1)
               {
               }
            cx.close();
            try
               {
               sc.close();
               }
            catch (IOException e1)
               {
               }
            return;
            }
         }
      }   
   }

