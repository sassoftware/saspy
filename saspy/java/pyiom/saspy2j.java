package pyiom;

import org.omg.CORBA.StringHolder;

import java.net.*;
import java.util.Arrays;

import java.io.IOException;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;

import com.sas.iom.SAS.ILanguageService;
import com.sas.iom.SAS.ILibref;
import com.sas.iom.SAS.IFileService;
import com.sas.iom.SAS.IFileref;
import com.sas.iom.SAS.IBinaryStream;
import com.sas.iom.SAS.IDataService;
import com.sas.iom.SAS.IWorkspace;
import com.sas.iom.SAS.IWorkspaceHelper;
import com.sas.iom.SAS.LNameNoAssign;
import com.sas.iom.SAS.IDataServicePackage.NoLibrary;
import com.sas.iom.SAS.StreamOpenMode;

import com.sas.iom.SASIOMCommon.IDisconnect;
import com.sas.iom.SASIOMCommon.IDisconnectHelper;
import com.sas.iom.SASIOMCommon.IDisconnectPackage.iomDisableFailed;
import com.sas.iom.SASIOMCommon.IDisconnectPackage.iomEnableFailed;
import com.sas.iom.SASIOMCommon.IDisconnectPackage.iomNoReconnectPortsAvailable;
import com.sas.iom.SASIOMCommon.IDisconnectPackage.iomReconnectDisabled;
import com.sas.iom.SASIOMCommon.IDisconnectPackage.iomReconnectInvalidTimeout;
import com.sas.iom.SASIOMCommon.IDisconnectPackage.iomReconnectNotAllowed;

import com.sas.iom.SASIOMDefs.*;
import com.sas.iom.orb.SASURI;

import com.sas.services.connection.BridgeServer;
import com.sas.services.connection.ConnectionFactoryConfiguration;
import com.sas.services.connection.ConnectionFactoryException;
import com.sas.services.connection.ConnectionFactoryInterface;
import com.sas.services.connection.ConnectionFactoryManager;
import com.sas.services.connection.ConnectionInterface;
import com.sas.services.connection.Credential;
import com.sas.services.connection.ManualConnectionFactoryConfiguration;
import com.sas.services.connection.Server;
import com.sas.services.connection.SecurityPackageCredential;
import com.sas.services.connection.ZeroConfigWorkspaceServer;

public class saspy2j
   {
   public saspy2j() {}

   static boolean         spn          = false;
   static int             timeout      = 60000;
   static int             filenum      = 1;
   static String          fn           = "_tomods"+filenum;
   static StringSeqHolder physicalName = new StringSeqHolder();

   static BufferedReader inp;
   static BufferedWriter outp;
   static BufferedWriter errp;

   static org.omg.CORBA.Object obj1      = null;
   static IDisconnect          iDisco1   = null;
   static String               uuid1     = null;
   static SASURI               uri       = null;
   static String               uriStr    = null;
   static String               reconStr  = null;
   static boolean              reconnect = false;

   static org.omg.CORBA.StringHolder qualUserNameHolder = null;
   static org.omg.CORBA.StringHolder genPasswordHolder  = null;

   static ConnectionFactoryConfiguration cxfConfig  = null;
   static ConnectionFactoryManager       cxfManager = null;
   static ConnectionFactoryInterface     cxf        = null;
   static Credential                     cred       = null;

   static ConnectionInterface cx      = null;
   static IWorkspace          wksp    = null;
   static ILanguageService    lang    = null;
   static IFileService        filesvc = null;
   static ILibref             libref  = null;
   static IFileref            fileref = null;
   static IFileref            upfref  = null;
   static IDataService        datasvc = null;
   static IBinaryStream       bstr    = null;
   static BridgeServer        server  = null;

   static Socket   sin      = null;
   static Socket   sout     = null;
   static Socket   serr     = null;
   static String   appName  = "";
   static String   iomhost  = "";
   static int      iomport  = 0;
   static String   omruser  = "";
   static String   omrpw    = "";
   static String   ad       = "";
   static String   physname = "";
   static int      hosts    = 0;
   static String[] iomhosts;
   static int      lrecl    = 32767;
   static int      logsz    = 32767;


   public static void main(String[] args) throws
                       InterruptedException, IOException, ConnectionFactoryException, GenericError
      {
      int inport  = 0;
      int outport = 0;
      int errport = 0;
      int len     = 0;
      int blen    = 0;
      int slen    = 0;
      int idx     = 0;
      int nargs   = args.length;
      long flen   = 0;

      String addr = "";
      String log  = "";
      String plog = "";
      String lst  = "";
      String pgm  = "";
      String eol  = "";

      boolean fndeol = false;
      boolean zero   = false;
      boolean ods    = false;
      boolean undo   = false;

      OctetSeqHolder odsdata = new OctetSeqHolder();
      char[]         in      = new char[4097];
      byte[]         out     = new byte[32768];

      for (int x = 0; x < nargs; x++)
         {
         if (args[x].equalsIgnoreCase("-host"))
            addr = args[x + 1];
         else if (args[x].equalsIgnoreCase("-stdinport"))
            inport = Integer.parseInt(args[x + 1]);
         else if (args[x].equalsIgnoreCase("-stdoutport"))
            outport = Integer.parseInt(args[x + 1]);
         else if (args[x].equalsIgnoreCase("-stderrport"))
            errport = Integer.parseInt(args[x + 1]);
         else if (args[x].equalsIgnoreCase("-iomhost"))
            iomhost = args[x + 1];
         else if (args[x].equalsIgnoreCase("-iomport"))
            iomport = Integer.parseInt(args[x + 1]);
         else if (args[x].equalsIgnoreCase("-timeout"))
            timeout = Integer.parseInt(args[x + 1]) * 1000;
         else if (args[x].equalsIgnoreCase("-user"))
            omruser = args[x + 1];
         else if (args[x].equalsIgnoreCase("-appname"))
            appName = args[x + 1];
         else if (args[x].equalsIgnoreCase("-zero"))
            zero = true;
         else if (args[x].equalsIgnoreCase("-spn"))
            spn = true;
         else if (args[x].equalsIgnoreCase("-lrecl"))
            lrecl = Integer.parseInt(args[x + 1]);
         else if (args[x].equalsIgnoreCase("-logbufsz"))
            logsz = Integer.parseInt(args[x + 1]);
         else if (args[x].equalsIgnoreCase("-uri"))
             reconStr = args[x + 1];
         }

      iomhosts = iomhost.split(";");
      hosts    = iomhosts.length;

      try
         {
         sin  = new Socket(addr, inport);
         sout = new Socket(addr, outport);
         serr = new Socket(addr, errport);
         }
      catch (IOException e)
         {
         e.printStackTrace();
         }

      OutputStream odsout = sout.getOutputStream();
      InputStream  odsin  = sout.getInputStream();

      inp  = new BufferedReader(new InputStreamReader(  sin.getInputStream(),  "UTF-8"));
      outp = new BufferedWriter(new OutputStreamWriter(sout.getOutputStream(), "UTF-8"));
      errp = new BufferedWriter(new OutputStreamWriter(serr.getOutputStream(), "UTF-8"));

      if (zero)
         {
         try
            {
            ZeroConfigWorkspaceServer            zserver = new ZeroConfigWorkspaceServer();
            ManualConnectionFactoryConfiguration config  = new ManualConnectionFactoryConfiguration(zserver);
            ConnectionFactoryManager             manager = new ConnectionFactoryManager();
            ConnectionFactoryInterface           factory = manager.getFactory(config);
            SecurityPackageCredential            zcred   = new SecurityPackageCredential();

            cx = factory.getConnection(zcred);

            connect(false, false, true);
            }
         catch (ConnectionFactoryException e)
            {
            String msg = "We failed in getConnection\n"+e.getMessage();
            errp.write(msg);
            errp.flush();
            System.out.print(msg);
            sin.close();
            sout.close();
            serr.close();
            e.printStackTrace();
            System.exit(-6);
            }
         }
      else
         {
         if (! spn && uriStr == null)
            omrpw = inp.readLine();
         connect(false, false, false);
         }

      while (true)
         {
         try
            {
            pgm = new String();
            while (true)
               {
               if ((idx = pgm.indexOf("tom says EOL=")) >= 0 && pgm.length() > idx + 13 + 32)
                  {
                  eol = pgm.substring(idx + 13, idx + 13 + 33);

                  if (eol.contains("UPLOAD"))
                     {
                     flen = Long.valueOf(pgm.substring(0, idx));
                     pgm  = pgm.substring(idx + 13 + 33);
               
                     bstr = null;
                     try
                        {
                        upfref  = filesvc.UseFileref("_sp_updn");
                        bstr = upfref.OpenBinaryStream(StreamOpenMode.StreamOpenModeForWriting);
                        }
                     catch (org.omg.CORBA.COMM_FAILURE e)
                        {
                        if (reconnect)
                           {
                           connect(true, false, false);
                           upfref  = filesvc.UseFileref("_sp_updn");
                           bstr = upfref.OpenBinaryStream(StreamOpenMode.StreamOpenModeForWriting);
                           }
                        }
                     catch (GenericError e)
                        {}
               
                     if (! (bstr == null))
                        {
                        while (flen > 0)
                           {
                           try
                              {
                              slen = odsin.read(out, 0, 32768);
                              if (slen > 0)
                                 {
                                 flen -= slen;
                                 bstr.Write(java.util.Arrays.copyOfRange(out, 0, slen));
                                 }
                              }
                           catch (org.omg.CORBA.COMM_FAILURE e)
                              {
                              if (reconnect)
                                 {
                                 ods = true;
                                 connect(true, true, false);
                                 bstr = fileref.OpenBinaryStream(StreamOpenMode.StreamOpenModeForWriting);
                                 bstr.Write(odsdata.value);
                                 }
                              else
                                 {
                                 String msg = "We failed in Submit\n"+e.getMessage();
                                 errp.write(msg);
                                 errp.flush();
                                 System.out.print(msg);
                                 e.printStackTrace();
                                 throw new IOException();
                                 }
                              }
                           catch (Exception e)
                              {
                              slen = 0; 
                              }
                           }
                        bstr.Close();
                        }
                     }
                  else if (eol.contains("DNLOAD"))
                     {
                     pgm  = pgm.substring(idx + 13 + 33);
               
                     bstr = null;
                     try
                        {
                        upfref  = filesvc.UseFileref("_sp_updn");
                        bstr = upfref.OpenBinaryStream(StreamOpenMode.StreamOpenModeForReading);
                        }
                     catch (org.omg.CORBA.COMM_FAILURE e)
                        {
                        if (reconnect)
                           {
                           connect(true, false, false);
                           upfref  = filesvc.UseFileref("_sp_updn");
                           bstr = upfref.OpenBinaryStream(StreamOpenMode.StreamOpenModeForReading);
                           }
                        }
                     catch (GenericError e)
                        {}

                     blen = 0;
                     slen = 1;

                     if (! (bstr == null))
                        {
                        while (slen > 0)
                           {
                           try
                              {
                              bstr.Read(9999999, odsdata);
                              slen = odsdata.value.length;
                              if (slen > 0)
                                 {
                                 blen += slen;
                                 odsout.write(odsdata.value);
                                 odsout.flush();
                                 }
                              }
                           catch (org.omg.CORBA.COMM_FAILURE e)
                              {
                              if (reconnect)
                                 {
                                 ods = true;
                                 connect(true, true, false);
                                 bstr = fileref.OpenBinaryStream(StreamOpenMode.StreamOpenModeForReading);
                                 bstr.Read(blen, odsdata);
                                 }
                              else
                                 {
                                 String msg = "We failed in Submit\n"+e.getMessage();
                                 errp.write(msg);
                                 errp.flush();
                                 System.out.print(msg);
                                 e.printStackTrace();
                                 throw new IOException();
                                 }
                              }
                           catch (Exception e)
                              {
                              slen = 0; 
                              }
                           }
                        bstr.Close();
                        }
                     }
                  else if (eol.contains("ASYNCH"))
                     {
                     try
                        {
                        lang.Submit(pgm.substring(0, idx));
                        pgm = pgm.substring(idx + 13 + 33);
                        }
                     catch (org.omg.CORBA.COMM_FAILURE e)
                        {
                        if (reconnect)
                           {
                           connect(true, false, false);
                           lang.Submit(pgm.substring(0, idx));
                           pgm = pgm.substring(idx + 13 + 33);
                           }
                        else
                           {
                           String msg = "We failed in Submit\n"+e.getMessage();
                           errp.write(msg);
                           errp.flush();
                           System.out.print(msg);
                           e.printStackTrace();
                           throw new IOException();
                           }
                        }
                     }
                  else if (eol.contains("DISCONNECT"))
                     {
                     if (reconnect)
                        {
                        cx.close();
                        errp.write("Succesfully disconnected. Be sure to have a valid network connection before submitting anything else.DISCONNECT");
                        errp.write(uriStr+"END_DISCON");
                        }
                     else
                        {
                        errp.write("This workspace server is not configured for reconnecting. Did not disconnect.DISCONNECT");
                        errp.write("END_DISCON");
                        }

                     errp.flush();
                     pgm = pgm.substring(idx + 13 + 33);

                     }
                  else if (eol.contains("ENDSAS"))
                     {
                     try
                        {
                        lang._release();
                        }
                     catch (org.omg.CORBA.COMM_FAILURE e)
                        {}

                     if (reconnect)
                        {
                        obj1    = cx.getObject();
                        iDisco1 = IDisconnectHelper.narrow(obj1);
                        try
                           {
                           iDisco1.DisableDisconnect();
                           }
                        catch (iomDisableFailed e)
                           {
                           try
                              {
                              cx.close();
                              server     = (BridgeServer) Server.fromURI(uri);
                              ad         = server.getDomain();
                    
                              if (appName != "")
                                 server.setServerName(appName.replace("\'", ""));
                              server.setOption(SASURI.applicationNameKey, "SASPy");
                              
                              cxfConfig  = new ManualConnectionFactoryConfiguration(server);
                              cxfManager = new ConnectionFactoryManager();
                              cxf        = cxfManager.getFactory(cxfConfig);
                              
                              if (spn)
                                 cx = cxf.getConnection(cred);
                              else
                                 cx = cxf.getConnection(omruser, omrpw, ad);
                              }
                           catch(ConnectionFactoryException e2)
                              {
                              String msg = "We failed reconnecting in ENDSAS. WUWT?\n"+e2.getMessage();
                              System.out.print(msg+"\n");
                              errp.write(msg+"\n");
                              errp.flush();
                              e2.printStackTrace();
                              }
                           }
                        }

                     cx.close();
                     sin.close();
                     sout.close();
                     serr.close();
                     return;
                     }
                  else if (eol.contains("PRINTTO"))
                     {
                     undo = true;
                     pgm  = pgm.substring(idx + 13 + 33);
                     }
                  else
                     {
                     pgm = pgm.substring(0, idx);
                     try{
                        lang.Submit(pgm);
                        if (undo)
                           lang.Submit("\nproc printto;run;\n%put "+eol.substring(1)+";\n");
                        else
                           lang.Submit("\n%put "+eol.substring(1)+";\n");
                        undo = false;
                        break;
                        }
                     catch(org.omg.CORBA.COMM_FAILURE e)
                        {
                        if (reconnect)
                           {
                           connect(true, false, false);
                           lang.Submit(pgm);
                           if (undo)
                              lang.Submit("\nproc printto;run;\n%put "+eol.substring(1)+";\n");
                           else
                              lang.Submit("\n%put "+eol.substring(1)+";\n");
                           undo = false;
                           break;
                           }
                        else
                           {
                           String msg = "We failed in Submit\n"+e.getMessage();
                           errp.write(msg);
                           errp.flush();
                           System.out.print(msg);
                           e.printStackTrace();
                           throw new IOException();
                           }
                        }
                     }
                  }
               else
                  {
                  len = inp.read(in, 0, 4096);
                  if (len > 0)
                     pgm += String.valueOf(Arrays.copyOfRange(in, 0, len));
                  }
               }

            blen = 0;
            slen = 1;
            bstr = null;
            try
               {
               bstr = fileref.OpenBinaryStream(StreamOpenMode.StreamOpenModeForReading);
               }
            catch (org.omg.CORBA.COMM_FAILURE e)
               {
               if (reconnect)
                  {
                  connect(true, false, false);
                  bstr = fileref.OpenBinaryStream(StreamOpenMode.StreamOpenModeForReading);
                  }
               }
            catch (GenericError e)
               {}

            if (! (bstr == null))
               {
               while (slen > 0)
                  {
                  try
                     {
                     bstr.Read(9999999, odsdata);
                     slen = odsdata.value.length;
                     if (slen > 0)
                        {
                        blen += slen;
                        odsout.write(odsdata.value);
                        odsout.flush();
                        }
                     }
                  catch (org.omg.CORBA.COMM_FAILURE e)
                     {
                     if (reconnect)
                        {
                        ods = true;
                        connect(true, true, false);
                        bstr = fileref.OpenBinaryStream(StreamOpenMode.StreamOpenModeForReading);
                        bstr.Read(blen, odsdata);
                        }
                     else
                        {
                        String msg = "We failed in Submit\n"+e.getMessage();
                        errp.write(msg);
                        errp.flush();
                        System.out.print(msg);
                        e.printStackTrace();
                        throw new IOException();
                        }
                     }
                  }
               bstr.Close();
               if (! ods)
                  fileref.DeleteFile();
               else
                  {
                  StringHolder retname = new StringHolder();
                  filenum ++;
                  fn       = "_tomods"+filenum;
                  physname = filesvc.FullName(fn, physicalName.value[0]);
                  fileref  = filesvc.AssignFileref(fn, "", physname, " lrecl="+lrecl, retname);
                  }
               }

            fndeol = false;
            while (true)
               {
               slen = 1;
               while (slen > 0)
                  {
                  try
                     {
                     lst  = lang.FlushList(9999999);
                     slen = lst.length();
                     if (slen > 0)
                        {
                        outp.write(lst);
                        outp.flush();
                        }
                     }
                  catch (org.omg.CORBA.COMM_FAILURE e)
                     {
                     if (reconnect)
                        connect(true, false, false);
                     else
                        {
                        String msg = "We failed in reading the List\n"+e.getMessage();
                        errp.write(msg);
                        errp.flush();
                        System.out.print(msg);
                        e.printStackTrace();
                        throw new IOException();
                        }
                     }
                  catch (IOException e)
                     {
                     String msg = "We failed in reading the List\n"+e.getMessage();
                     errp.write(msg);
                     errp.flush();
                     System.out.print(msg);
                     sin.close();
                     sout.close();
                     serr.close();
                     e.printStackTrace();
                     break;
                     }
                  }

                  if (fndeol)
                     break;

                  slen = 1;
                  while (slen > 0)
                     {
                     try
                        {
                        log  = lang.FlushLog(logsz);
                        slen = log.length();
                        if (slen > 0)
                           {
                           errp.write(log);
                           errp.flush();

                           if ((plog+log).contains(eol))
                              {
                              outp.write(eol);
                              if (ods)
                                 {
                                 outp.write(fn);
                                 ods = false;
                                 }
                              outp.flush();
                              fndeol = true;
                              }
                           plog = log;
                           }
                        }
                     catch (org.omg.CORBA.COMM_FAILURE e)
                        {
                        if (reconnect)
                           connect(true, false, false);
                        else
                           {
                           String msg = "We failed in reading the Log\n"+e.getMessage();
                           errp.write(msg);
                           errp.flush();
                           System.out.print(msg);
                           e.printStackTrace();
                           throw new IOException();
                           }
                        }
                     catch (IOException e)
                        {
                        String msg = "We failed in reading the Log\n"+e.getMessage();
                        errp.write(msg);
                        errp.flush();
                        System.out.print(msg);
                        sin.close();
                        sout.close();
                        serr.close();
                        e.printStackTrace();
                        break;
                        }
                     catch (org.omg.CORBA.DATA_CONVERSION e)
                        {
                        String msg = "We failed in reading the Log\n"+e.getMessage();
                        errp.write(msg);
                        errp.flush();
                        lang.Submit("%put "+eol.substring(1)+";\n");
                        slen = 1;
                        continue;
                        }
                     }
                  }
               }
          catch (GenericError e)
             {
             String msg = "We failed in outer loop\n"+e.getMessage();
             errp.write(msg);
             errp.flush();
             System.out.print(msg);
             sin.close();
             sout.close();
             serr.close();
             e.printStackTrace();
             break;
             }
          }
      }

private static void connect(boolean recon, boolean ods, boolean zero) throws IOException, ConnectionFactoryException, GenericError
   {
    boolean                       failed             = false;
    boolean[]                     fieldInclusionMask = new boolean[0];
    StringHolder                  retname            = new StringHolder();
    LongSeqHolder                 libraryAttrs       = new LongSeqHolder();
    StringSeqHolder               engineName         = new StringSeqHolder();
    VariableArray2dOfLongHolder   engineAttrs        = new VariableArray2dOfLongHolder();
    VariableArray2dOfStringHolder infoPropertyNames  = new VariableArray2dOfStringHolder();
    VariableArray2dOfStringHolder infoPropertyValues = new VariableArray2dOfStringHolder();

    if (reconStr != null)
       {
       uri      = SASURI.create(reconStr);
       recon    = true;
       reconStr = null;
       }

    if (! zero)
       {
       if (recon)
          {
          try
             {
             server     = (BridgeServer) Server.fromURI(uri);
             ad         = server.getDomain();
             if (appName != "")
                server.setServerName(appName.replace("\'", ""));
             server.setOption(SASURI.applicationNameKey, "SASPy");
   
             cxfConfig  = new ManualConnectionFactoryConfiguration(server);
             cxfManager = new ConnectionFactoryManager();
             cxf        = cxfManager.getFactory(cxfConfig);
   
             if (spn)
                cx = cxf.getConnection(cred);
             else if (timeout > 0)
                cx = cxf.getConnection(omruser, omrpw, ad, timeout);
             else
                cx = cxf.getConnection(omruser, omrpw, ad);
             }
          catch(ConnectionFactoryException e)
             {
             String msg = "We failed in getConnection\n"+e.getMessage();
             System.out.print(msg+"\n");
             errp.write(msg+"\n");
             errp.flush();
             e.printStackTrace();
             failed = true;
             }
          }
       else
          {
          for (int i=0; i < hosts; i++)
             {
             try
                {
                server = new BridgeServer(Server.CLSID_SAS, iomhosts[i], iomport);
                if (appName != "")
                   server.setServerName(appName.replace("\'", ""));
                server.setOption(SASURI.applicationNameKey, "SASPy");
   
                if (spn)
                   server.setSecurityPackage(Server.SECURITY_PACKAGE_NEGOTIATE);
   
                cxfConfig  = new ManualConnectionFactoryConfiguration(server);
                cxfManager = new ConnectionFactoryManager();
                cxf        = cxfManager.getFactory(cxfConfig);
   
                if (spn)
                   {
                   cred = SecurityPackageCredential.getInstance();
                   cx   = cxf.getConnection(cred);
                   }
                else if (timeout > 0)
                   cx = cxf.getConnection(omruser, omrpw, timeout);
                else
                   cx = cxf.getConnection(omruser, omrpw);
                break;
                }
             catch (ConnectionFactoryException e)
                {
                if (i+1 < hosts)
                   continue;
                String msg = "We failed in getConnection\n"+e.getMessage();
                System.out.print(msg+"\n");
                errp.write(msg+"\n");
                errp.flush();
                failed = true;
                }
             }
          }
       }

    if (!failed)
       {
       obj1    = cx.getObject();
       iDisco1 = IDisconnectHelper.narrow(obj1);
       try
          {
          uriStr    = iDisco1.EnableDisconnect(0,false);
          uri       = SASURI.create(uriStr);
          reconnect = true;
          }
       catch (iomReconnectNotAllowed | iomReconnectInvalidTimeout | iomReconnectDisabled |
                     iomEnableFailed | iomNoReconnectPortsAvailable | GenericError e1)
          {
          reconnect = false;
          }

       try
          {
          wksp    = IWorkspaceHelper.narrow(obj1);
          uuid1   = wksp.UniqueIdentifier();
          lang    = wksp.LanguageService();
          filesvc = wksp.FileService();
          datasvc = wksp.DataService();
          }
       catch (Exception e)
          {
          String msg = "We failed in getConnection\n"+e.getMessage();
          System.out.print(msg+"\n");
          errp.write(msg+"\n");
          errp.flush();
          e.printStackTrace();
          }

       try
          {
          if (! recon)
             {
             libref = datasvc.UseLibref("work");
             libref.LevelInfo(fieldInclusionMask, engineName, engineAttrs, libraryAttrs,
                                  physicalName, infoPropertyNames, infoPropertyValues);
             physname = filesvc.FullName(fn, physicalName.value[0]);
             fileref  = filesvc.AssignFileref(fn, "", physname, " lrecl="+lrecl, retname);
             }
          else
             fileref  = filesvc.UseFileref(fn);
          }
       catch (GenericError | LNameNoAssign | NoLibrary e)
          {
          String msg = "We failed in getConnection\n"+e.getMessage();
          System.out.print(msg+"\n");
          errp.write(msg+"\n");
          errp.flush();
          e.printStackTrace();
          }
       }
    else
       {
       sin.close();
       sout.close();
       serr.close();
       System.exit(-6);
       }
   }
}
