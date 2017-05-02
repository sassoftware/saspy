package pyiom;

import java.io.IOException;
import java.net.*;
//import java.nio.ByteBuffer;
import java.util.Arrays;

import org.omg.CORBA.StringHolder;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

import com.sas.iom.SAS.ILanguageService;
import com.sas.iom.SAS.ILibref;
import com.sas.iom.SAS.IFileService;
import com.sas.iom.SAS.IFileref;
import com.sas.iom.SAS.IBinaryStream;
import com.sas.iom.SAS.IDataService;
import com.sas.iom.SAS.IWorkspace;
import com.sas.iom.SAS.IWorkspaceHelper;
import com.sas.iom.SAS.InvalidFieldMask;
import com.sas.iom.SAS.LNameNoAssign;
import com.sas.iom.SAS.IDataServicePackage.NoLibrary;
import com.sas.iom.SAS.IFileServicePackage.AssignmentContextSeqHolder;
import com.sas.iom.SASIOMDefs.*;
import com.sas.iom.orb.SASURI;
import com.sas.services.connection.BridgeServer;
//import com.sas.services.connection.ConnectionFactoryAdminInterface;
import com.sas.services.connection.ConnectionFactoryConfiguration;
import com.sas.services.connection.ConnectionFactoryException;
import com.sas.services.connection.ConnectionFactoryInterface;
import com.sas.services.connection.ConnectionFactoryManager;
import com.sas.services.connection.ConnectionInterface;
import com.sas.services.connection.ManualConnectionFactoryConfiguration;
import com.sas.services.connection.Server;

import com.sas.services.connection.SecurityPackageCredential;
import com.sas.services.connection.ZeroConfigWorkspaceServer;

import com.sas.iom.SAS.StreamOpenMode;

public class saspy2j {
        public saspy2j() {
        }

        public static void main(String[] args) throws InterruptedException, IOException, ConnectionFactoryException {
                int inport = 0;
                int outport = 0;
                int errport = 0;
                int iomport = 0;
                int timeout = 60000;
                int len = 0;
                int slen = 0;
                int nargs = args.length;
                String addr = "";
                Socket sin = null;
                Socket sout = null;
                Socket serr = null;
                String appName = "";
                String iomhost = "";
                String omruser = "";
                String omrpw = "";
                char[] in = new char[4097];
                String log = "";
                String lst = "";
                String pgm;
                String eol = "";
                int idx = 0;
                boolean fndeol;
                boolean zero = false;
                boolean failed = false;

                BufferedReader inp;
                BufferedWriter outp;
                BufferedWriter errp;

                ConnectionInterface cx = null;
                IWorkspace        wksp = null;
                ILanguageService  lang = null;
                IFileService   filesvc = null;
                ILibref         libref = null;
                IFileref       fileref = null;
                IDataService   datasvc = null;
                IBinaryStream     bstr = null;
                OctetSeqHolder odsdata = null;
                BridgeServer    server = null;

                // System.out.print("localhost="+InetAddress.getLocalHost()+'\n');
                // System.out.print("nargs="+nargs+'\n');
                for (int x = 0; x < nargs; x++) {
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
                }

                try {
                        sin = new Socket(addr, inport);
                        sout = new Socket(addr, outport);
                        serr = new Socket(addr, errport);
                } catch (IOException e) {
                        e.printStackTrace();
                }

                inp = new BufferedReader(new InputStreamReader(sin.getInputStream()));
                outp = new BufferedWriter(new OutputStreamWriter(sout.getOutputStream()));
                errp = new BufferedWriter(new OutputStreamWriter(serr.getOutputStream()));

                if (zero) {
                        try {
                                ZeroConfigWorkspaceServer zserver = new ZeroConfigWorkspaceServer();
                                ManualConnectionFactoryConfiguration config = new ManualConnectionFactoryConfiguration(zserver);
                                ConnectionFactoryManager manager = new ConnectionFactoryManager();
                                ConnectionFactoryInterface factory = manager.getFactory(config);
                                SecurityPackageCredential cred = new SecurityPackageCredential();
                                cx = factory.getConnection(cred);
                        } catch (ConnectionFactoryException e) {
                                String msg = e.getMessage();
                                errp.write(msg);
                                errp.flush();
                                System.out.print(msg);
                                failed = true;
                        }

                } else {
                        omrpw = inp.readLine();
                        try {
                                server = new BridgeServer(Server.CLSID_SAS, iomhost, iomport);
                                if (appName != "")
                                   server.setServerName(appName.replace("\'", ""));
                                //server.setOption(SASURI.applicationNameKey, appName);
                                ConnectionFactoryConfiguration cxfConfig = new ManualConnectionFactoryConfiguration(server);
                                ConnectionFactoryManager cxfManager = new ConnectionFactoryManager();
                                ConnectionFactoryInterface cxf = cxfManager.getFactory(cxfConfig);
                                // ConnectionFactoryAdminInterface admin =
                                // cxf.getAdminInterface();
                                if (timeout > 0)
                                   cx = cxf.getConnection(omruser, omrpw, timeout);
                                else
                                   cx = cxf.getConnection(omruser, omrpw);
                        } catch (ConnectionFactoryException e) {
                                String msg = e.getMessage();
                                errp.write("AppName=");
                                errp.write(appName);
                                errp.write(msg);
                                errp.flush();
                                System.out.print(msg);
                                failed = true;
                        }
                }

                if (!failed) {
                        wksp = IWorkspaceHelper.narrow(cx.getObject());
                        lang = wksp.LanguageService();
                        filesvc = wksp.FileService();
                        datasvc = wksp.DataService();

                        try {
                                libref = datasvc.UseLibref("work");
                                boolean[] fieldInclusionMask = new boolean[0];
                                StringSeqHolder engineName = new StringSeqHolder();
                                VariableArray2dOfLongHolder engineAttrs = new VariableArray2dOfLongHolder();
                                LongSeqHolder libraryAttrs = new LongSeqHolder();
                                StringSeqHolder physicalName = new StringSeqHolder();
                                VariableArray2dOfStringHolder infoPropertyNames = new VariableArray2dOfStringHolder();
                                VariableArray2dOfStringHolder infoPropertyValues = new VariableArray2dOfStringHolder();

                                libref.LevelInfo(fieldInclusionMask, engineName, engineAttrs, libraryAttrs, physicalName,
                                                infoPropertyNames, infoPropertyValues);
                                // System.out.println(physicalName.value[0]);
                                StringHolder retname = new StringHolder();
                                // filesvc.MakeDirectory(physicalName.value[0], "tomods1");
                                fileref = filesvc.AssignFileref("_tomods1", "", filesvc.FullName("tomods1", physicalName.value[0]), "encoding=\"utf-8\"",
                                                retname);

                                boolean[] arg0 = new boolean[0];
                                StringSeqHolder arg1 = new StringSeqHolder();
                                AssignmentContextSeqHolder arg2 = new AssignmentContextSeqHolder();
                                StringSeqHolder arg3 = new StringSeqHolder();
                                StringSeqHolder arg4 = new StringSeqHolder();
                                filesvc.ListFilerefs(arg0, arg1, arg2, arg3, arg4);
                                // System.out.println(arg3.value[0]);

                        } catch (GenericError | InvalidFieldMask | LNameNoAssign | NoLibrary e) {
                                e.printStackTrace();
                        }
                }

                odsdata = new OctetSeqHolder();
                while (true) {
                        try {
                                pgm = new String();
                                while (true) {
                                        if ((idx = pgm.indexOf("tom says EOL=")) >= 0 && pgm.length() > idx + 13 + 32) {
                                                eol = pgm.substring(idx + 13, idx + 13 + 33);

                                                if (failed) {
                                                        errp.write(eol);
                                                        errp.flush();
                                                        sin.close();
                                                        sout.close();
                                                        serr.close();
                                                        System.exit(-6);
                                                }

                                                if (eol.contains("ASYNCH")) {
                                                        lang.Submit(pgm.substring(0, idx));
                                                        pgm = pgm.substring(idx + 13 + 33);
                                                } else if (eol.contains("ENDSAS")) {
                                                        lang._release();
                                                        cx.close();
                                                        return;
                                                } else {
                                                        pgm = pgm.substring(0, idx);
                                                        // System.out.println(pgm);
                                                        lang.Submit(pgm);
                                                        break;
                                                }
                                        } else {
                                                len = inp.read(in, 0, 4096);
                                                // System.out.println(len);
                                                if (len > 0) {
                                                        pgm += String.valueOf(Arrays.copyOfRange(in, 0, len));
                                                }
                                        }
                                }

                                try {
                                        slen = 1;
                                        bstr = fileref.OpenBinaryStream(StreamOpenMode.StreamOpenModeForReading);
                                        try {
                                                while (slen > 0) {
                                                        bstr.Read(9999999, odsdata);
                                                        String s = new String(odsdata.value);
                                                        slen = s.length();
                                                        if (slen > 0) {
                                                                outp.write(s);
                                                                outp.flush();
                                                        }
                                                }
                                        } catch (IOException e) {
                                                sin.close();
                                                sout.close();
                                                serr.close();
                                                break;
                                        }
                                        bstr.Close();
                                        fileref.DeleteFile();
                                } catch (GenericError e) {
                                }

                                fndeol = false;
                                while (true) {
                                        slen = 1;
                                        try {
                                                while (slen > 0) {
                                                        lst = lang.FlushList(9999999);
                                                        slen = lst.length();
                                                        if (slen > 0) {
                                                                outp.write(lst);
                                                                outp.flush();
                                                        }
                                                }
                                        } catch (IOException e) {
                                                sin.close();
                                                sout.close();
                                                serr.close();
                                                break;
                                        }

                                        if (fndeol)
                                                break;

                                        slen = 1;
                                        try {
                                                while (slen > 0) {
                                                        log = lang.FlushLog(9999999);
                                                        slen = log.length();
                                                        if (slen > 0) {
                                                                errp.write(log);
                                                                errp.flush();

                                                                if (log.contains(eol)) {
                                                                        outp.write(eol);
                                                                        outp.flush();
                                                                        fndeol = true;
                                                                }
                                                        }
                                                }
                                        } catch (IOException e) {
                                                sin.close();
                                                sout.close();
                                                serr.close();
                                                break;
                                        }
                                }
                        } catch (GenericError e) {
                                sin.close();
                                sout.close();
                                serr.close();
                                e.printStackTrace();
                        }
                }
        }
}
