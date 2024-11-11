import './App.css'
import TwitterFollowCard from './TwitterFollowCard'

export default function App(){

  return (
    <section className='App'>
    <TwitterFollowCard  
      initialIsFollowing userName="midudev" name="Miguel Angel Duran">
        Miguel Angel Duran
    </TwitterFollowCard>

    <TwitterFollowCard  
      initialIsFollowing={false} userName="pheralb" name="Pablo Hernandez">
        Pablo Hernandez
    </TwitterFollowCard>

    <TwitterFollowCard  
      initialIsFollowing userName="vxnder" name="Vanderhart">
        Vanderhart
    </TwitterFollowCard>
    </section>
  );
}
