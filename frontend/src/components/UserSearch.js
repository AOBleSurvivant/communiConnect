import React, { useState, useEffect } from 'react';
import { 
    Box, 
    Input, 
    VStack, 
    HStack, 
    Text, 
    Avatar, 
    Button, 
    Badge,
    Spinner,
    Alert,
    AlertIcon,
    useToast,
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalBody,
    ModalFooter,
    useDisclosure
} from '@chakra-ui/react';
import { SearchIcon, AddIcon, CheckIcon, CloseIcon } from '@chakra-ui/icons';
import { useAuth } from '../contexts/AuthContext';

const UserSearch = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(false);
    const [selectedUser, setSelectedUser] = useState(null);
    const { isOpen, onOpen, onClose } = useDisclosure();
    const { token } = useAuth();
    const toast = useToast();

    const searchUsers = async (query) => {
        if (!query.trim()) {
            setUsers([]);
            return;
        }

        setLoading(true);
        try {
            const response = await fetch(`/api/users/search/?q=${encodeURIComponent(query)}`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                setUsers(data);
            } else {
                throw new Error('Erreur lors de la recherche');
            }
        } catch (error) {
            toast({
                title: 'Erreur',
                description: error.message,
                status: 'error',
                duration: 3000,
                isClosable: true,
            });
        } finally {
            setLoading(false);
        }
    };

    const followUser = async (userId) => {
        try {
            const response = await fetch('/api/users/follow/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_id: userId }),
            });

            if (response.ok) {
                const data = await response.json();
                toast({
                    title: 'Succès',
                    description: data.message,
                    status: 'success',
                    duration: 3000,
                    isClosable: true,
                });
                
                // Mettre à jour la liste des utilisateurs
                setUsers(users.map(user => 
                    user.id === userId 
                        ? { ...user, is_following: true, can_follow: false }
                        : user
                ));
            } else {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Erreur lors de l\'ajout');
            }
        } catch (error) {
            toast({
                title: 'Erreur',
                description: error.message,
                status: 'error',
                duration: 3000,
                isClosable: true,
            });
        }
    };

    const unfollowUser = async (userId) => {
        try {
            const response = await fetch('/api/users/unfollow/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_id: userId }),
            });

            if (response.ok) {
                const data = await response.json();
                toast({
                    title: 'Succès',
                    description: data.message,
                    status: 'success',
                    duration: 3000,
                    isClosable: true,
                });
                
                // Mettre à jour la liste des utilisateurs
                setUsers(users.map(user => 
                    user.id === userId 
                        ? { ...user, is_following: false, can_follow: true }
                        : user
                ));
            } else {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Erreur lors de la suppression');
            }
        } catch (error) {
            toast({
                title: 'Erreur',
                description: error.message,
                status: 'error',
                duration: 3000,
                isClosable: true,
            });
        }
    };

    const handleUserClick = (user) => {
        setSelectedUser(user);
        onOpen();
    };

    useEffect(() => {
        const timeoutId = setTimeout(() => {
            if (searchQuery.trim()) {
                searchUsers(searchQuery);
            }
        }, 500);

        return () => clearTimeout(timeoutId);
    }, [searchQuery]);

    return (
        <Box p={4}>
            <VStack spacing={4} align="stretch">
                <Box>
                    <Text fontSize="xl" fontWeight="bold" mb={2}>
                        Rechercher des utilisateurs
                    </Text>
                    <Input
                        placeholder="Rechercher par nom, prénom ou email..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        size="lg"
                        pr="4.5rem"
                    />
                </Box>

                {loading && (
                    <Box textAlign="center" py={4}>
                        <Spinner size="lg" />
                        <Text mt={2}>Recherche en cours...</Text>
                    </Box>
                )}

                {!loading && users.length > 0 && (
                    <VStack spacing={3} align="stretch">
                        <Text fontSize="md" fontWeight="semibold">
                            Résultats ({users.length})
                        </Text>
                        {users.map((user) => (
                            <Box
                                key={user.id}
                                p={4}
                                border="1px"
                                borderColor="gray.200"
                                borderRadius="md"
                                cursor="pointer"
                                _hover={{ bg: 'gray.50' }}
                                onClick={() => handleUserClick(user)}
                            >
                                <HStack justify="space-between">
                                    <HStack spacing={3}>
                                        <Avatar
                                            size="md"
                                            name={user.full_name}
                                            src={user.profile_picture}
                                        />
                                        <VStack align="start" spacing={1}>
                                            <Text fontWeight="bold">
                                                {user.full_name}
                                            </Text>
                                            <Text fontSize="sm" color="gray.600">
                                                @{user.username}
                                            </Text>
                                            {user.quartier && (
                                                <Badge colorScheme="blue" size="sm">
                                                    {user.quartier.nom}
                                                </Badge>
                                            )}
                                        </VStack>
                                    </HStack>
                                    
                                    <Button
                                        size="sm"
                                        colorScheme={user.is_following ? "red" : "blue"}
                                        leftIcon={user.is_following ? <CloseIcon /> : <AddIcon />}
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            if (user.is_following) {
                                                unfollowUser(user.id);
                                            } else {
                                                followUser(user.id);
                                            }
                                        }}
                                        isDisabled={!user.can_follow && !user.is_following}
                                    >
                                        {user.is_following ? 'Ne plus suivre' : 'Suivre'}
                                    </Button>
                                </HStack>
                            </Box>
                        ))}
                    </VStack>
                )}

                {!loading && searchQuery && users.length === 0 && (
                    <Alert status="info">
                        <AlertIcon />
                        Aucun utilisateur trouvé pour "{searchQuery}"
                    </Alert>
                )}

                {/* Modal pour les détails de l'utilisateur */}
                <Modal isOpen={isOpen} onClose={onClose} size="md">
                    <ModalOverlay />
                    <ModalContent>
                        <ModalHeader>Profil de {selectedUser?.full_name}</ModalHeader>
                        <ModalBody>
                            {selectedUser && (
                                <VStack spacing={4} align="start">
                                    <HStack spacing={4}>
                                        <Avatar
                                            size="xl"
                                            name={selectedUser.full_name}
                                            src={selectedUser.profile_picture}
                                        />
                                        <VStack align="start" spacing={1}>
                                            <Text fontSize="xl" fontWeight="bold">
                                                {selectedUser.full_name}
                                            </Text>
                                            <Text color="gray.600">
                                                @{selectedUser.username}
                                            </Text>
                                            {selectedUser.quartier && (
                                                <Badge colorScheme="blue">
                                                    {selectedUser.quartier.nom}
                                                </Badge>
                                            )}
                                        </VStack>
                                    </HStack>
                                    
                                    {selectedUser.bio && (
                                        <Box>
                                            <Text fontWeight="semibold" mb={2}>
                                                Bio
                                            </Text>
                                            <Text>{selectedUser.bio}</Text>
                                        </Box>
                                    )}
                                    
                                    <HStack spacing={4}>
                                        <VStack spacing={1}>
                                            <Text fontSize="lg" fontWeight="bold">
                                                {selectedUser.followers_count}
                                            </Text>
                                            <Text fontSize="sm" color="gray.600">
                                                Abonnés
                                            </Text>
                                        </VStack>
                                        <VStack spacing={1}>
                                            <Text fontSize="lg" fontWeight="bold">
                                                {selectedUser.following_count}
                                            </Text>
                                            <Text fontSize="sm" color="gray.600">
                                                Abonnements
                                            </Text>
                                        </VStack>
                                    </HStack>
                                </VStack>
                            )}
                        </ModalBody>
                        <ModalFooter>
                            <Button colorScheme="blue" mr={3} onClick={onClose}>
                                Fermer
                            </Button>
                            {selectedUser && (
                                <Button
                                    colorScheme={selectedUser.is_following ? "red" : "blue"}
                                    leftIcon={selectedUser.is_following ? <CloseIcon /> : <AddIcon />}
                                    onClick={() => {
                                        if (selectedUser.is_following) {
                                            unfollowUser(selectedUser.id);
                                        } else {
                                            followUser(selectedUser.id);
                                        }
                                        onClose();
                                    }}
                                    isDisabled={!selectedUser.can_follow && !selectedUser.is_following}
                                >
                                    {selectedUser.is_following ? 'Ne plus suivre' : 'Suivre'}
                                </Button>
                            )}
                        </ModalFooter>
                    </ModalContent>
                </Modal>
            </VStack>
        </Box>
    );
};

export default UserSearch; 