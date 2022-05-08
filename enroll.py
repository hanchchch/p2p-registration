from enroll import EnrollClient, ProjectTypes

if __name__ == "__main__":
    client = EnrollClient(
        project=ProjectTypes.Gossip,
        email="hanc@in.tum.de",
        firstname="Chung Hwan",
        lastname="Han",
        gitlab_username="00000000014B2B22",
    )
    client.run()
