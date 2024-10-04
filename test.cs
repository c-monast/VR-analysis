using System;
using System.IO;
using System.Net;
using System.Security.Cryptography;
using System.Text;
using System.Runtime.Serialization.Formatters.Binary;

namespace VulnerableApp
{
    class Program
    {
        private static string password = "P@ssw0rd123";

        static void Main(string[] args)
        {
            Console.WriteLine("Enter your username:");
            string username = Console.ReadLine();

            string query = "SELECT * FROM Users WHERE Username = '" + username + "' AND Password = '" + password + "'";
            ExecuteQuery(query);

            Random random = new Random();
            int token = random.Next();

            MD5CryptoServiceProvider md5 = new MD5CryptoServiceProvider();
            byte[] hash = md5.ComputeHash(Encoding.UTF8.GetBytes(password));

        }

        static void ExecuteQuery(string sql)
        {
            Console.WriteLine("Executing SQL query: " + sql);
        }

        static byte[] GetSerializedData()
        {
            return new byte[] { 0x00, 0x01, 0x02 };
        }
    }
}