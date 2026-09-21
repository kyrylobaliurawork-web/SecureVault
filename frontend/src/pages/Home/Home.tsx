import Navbar from "../../components/Navbar/Navbar";
import FileTable from "../../components/FileTable/FileTable";

function Home() {
  return (
    <div className="home">
      <Navbar />

      <main className="home-content">
        <FileTable />
      </main>
    </div>
  );
}

export default Home;